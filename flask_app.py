from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import random

app = Flask(__name__)
selected_channel = []
video_search_results = []
video_limit = 5
channel_limit = 3

def channel_search(channel_text): 
#-- returns (2): (1) LIST of channel info of all matching results if there are YT channels found, (2) None if no channels found

    for x in ["", " channel"," ch"," TV"]: #sometimes YT search doesn't return desired channel name even if EXACT channel name (that has japanese text) is inputted 
        search_query_ch = requests.get("https://www.youtube.com/results?search_query={}".format(channel_text + x))
        html_chunk_ch = BeautifulSoup(search_query_ch.content,"html.parser")
        find_channelRenderer = [x for x in html_chunk_ch.find_all("script") if 'channelRenderer' in str(x)]

        if len(find_channelRenderer) > 0:
            json_split_ch = str(find_channelRenderer[0]).split('var ytInitialData = ')[1].split(';</script>')[0]
            final_json_ch = json.loads(json_split_ch)
            names = [x["channelRenderer"]["title"]["simpleText"] for x in final_json_ch["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] if 'channelRenderer' in x] #if 'channelRenderer' to filter out playListRenderer
            idstring = [x["channelRenderer"]["channelId"] for x in final_json_ch["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] if 'channelRenderer' in x]
            thumbnail = [x["channelRenderer"]["thumbnail"]["thumbnails"][0]["url"] for x in final_json_ch["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] if 'channelRenderer' in x]
            subs = [
                x["channelRenderer"]["subscriberCountText"]["simpleText"] if "subscriberCountText" in x["channelRenderer"] else "0 Subscribers" #channel search results that have no subscribers
                for x in 
                final_json_ch["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] 
                if 'channelRenderer' in x 
                ]
            vids = [
                str(x["channelRenderer"]["videoCountText"]["runs"][0]["text"]) + " Videos" if "videoCountText" in x["channelRenderer"] else "0 Videos" #channel search results that have no uploads
                for x in 
                final_json_ch["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] 
                if 'channelRenderer' in x 
                ]
            for x in list(zip(names,thumbnail)):
                print(x)
            zipped = list(zip(names,idstring,thumbnail,subs,vids))
            break
        else:
            zipped = None
            continue

    return zipped

def video_search(channel_id, video_text):
#-- returns (2): (1) DICTIONARY of one channel and multiple video info if there are videos found, (2) None if no videos found
    search_query = requests.get("https://www.youtube.com/channel/{}/search?query={}".format(channel_id,video_text))
    html_chunk = BeautifulSoup(search_query.content,"html.parser")
    find_videoRenderer = [x for x in html_chunk.find_all("script") if 'videoRenderer' in str(x)]

    if len(find_videoRenderer) > 0:
        json_split = str(find_videoRenderer[0]).split('var ytInitialData = ')[1].split(';</script>')[0]
        final_json = json.loads(json_split)
        sectionListRenderer_contents = final_json["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][6]["expandableTabRenderer"]["content"]["sectionListRenderer"]["contents"]
        limit_items = [x[1] for x in list(enumerate(sectionListRenderer_contents)) if x[0] < video_limit and "playlistRenderer" not in str(x[1])] #limits video results to 'video_limit' and filters out playlist content
        itemSectionRenderer_contents = [x["itemSectionRenderer"]["contents"][0]["videoRenderer"] for x in limit_items]

        channel = final_json["microformat"]["microformatDataRenderer"]["title"]
        channel_url = final_json["microformat"]["microformatDataRenderer"]["urlCanonical"] #contains actual url with 'https://www.youtube.com.....
        """
        videos_found contents:

        title          【APEX】あくたんに守られたいあぺ【ホロライブ / 星街すいせい】', 
        video id       'Razjoh7c_Ek', 
        thumbnail url  'https://i.ytimg.com/vi/Razjoh7c_Ek/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDCnW5XmScEHaIv-_xiQffd5cN7Xg',
        view count     '453K views',
        putblish time  '10 months ago'
        """
        title = [x["title"]["runs"][0]["text"] for x in itemSectionRenderer_contents]
        video_url = [x["videoId"] for x in itemSectionRenderer_contents]
        thumbnail = [x["thumbnail"]["thumbnails"][3]["url"] for x in itemSectionRenderer_contents]
        views = [
                x["viewCountText"]["simpleText"] if "viewCountText" in x and "simpleText" in x["viewCountText"] else "0 Views" #for future scheduled uploads which are always at 0 views
                for x in 
                itemSectionRenderer_contents
                ]
        published = [
                    x["publishedTimeText"]["simpleText"] if "publishedTimeText" in x and "simpleText" in x["publishedTimeText"] else "Unpublished" #for future scheduled uploads which are not published yet
                    for x in 
                    itemSectionRenderer_contents
                    ]

        dict_entry = {
            "channel_name":channel,
            "channel_url":channel_url,
            "videos_found": list(zip(title,video_url,thumbnail,views,published))
        }
        return dict_entry
    else:
        return None #No content from channel_id matched video_text

def selected_channel_state(x):
    if x:
        return True
    else:
        return False

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == "POST":
        if "input_box_channel" in request.form:
            channel_input = request.form["input_box_channel"]
            if len(selected_channel) < 5:
                if channel_input != '':
                    search_results_ch = channel_search(channel_input)
                    if search_results_ch != None:
                        return render_template("index2.html", channelresults = search_results_ch, selectedchannels = selected_channel, show_section_B = True, show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel))
                    else:
                        return render_template("index2.html", emptymessage_ch = "No channel found. Please try again.", selectedchannels = selected_channel, show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel))
                else:
                    return render_template("index2.html", emptymessage_ch = "Invalid input.", selectedchannels = selected_channel, show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel))
            else:
                return render_template("index2.html", emptymessage_ch = "For this is just a demo, selection is limited to 5 channels. Please proceed to video search.", selectedchannels = selected_channel, show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel), disable_input = True)       
        elif "channelradio" in request.form:
            channel_selected = request.form["channelradio"]
            if channel_selected in [x[0] for x in selected_channel]:
                return render_template("index2.html", selectedchannels = selected_channel, show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel))
            else:
                channel_info = channel_search(channel_selected)
                if len(selected_channel) < 5:
                    selected_channel.append([x for x in channel_info[0]])
                    return render_template("index2.html", selectedchannels = selected_channel, show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel))
                else:
                    return render_template("index2.html", emptymessage_ch = "For this is just a demo, selection is limited to 5 channels. Please proceed to video search.", selectedchannels = selected_channel, show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel), disable_input = True)
    else:
        selected_channel.clear()
        video_search_results.clear()
        return render_template("index2.html")

@app.route('/search-results', methods=['GET','POST'])
def video_submit():
    video_input = request.form["input_box_video"]
    if video_input != '':
        for x in [z for z in selected_channel]:
            n = random.random() + 2
            sleep(n)
            search_results_vid = video_search(x[1], video_input)
            if search_results_vid != None:
                video_search_results.append(video_search(x[1], video_input))
            else:
                video_search_results.append({"channel_name":x[0],"channel_url":f"https://www.youtube.com/channel/{x[1]}","videos_found":None})
        return render_template("search_results.html", videoresults = video_search_results, channels = selected_channel, user_input = video_input)
    else:
        return render_template("index2.html", selectedchannels = selected_channel, emptymessage_vid = "Invalid input.", show_section_B = False , show_section_C = selected_channel_state(selected_channel), show_section_D = selected_channel_state(selected_channel))

@app.route('/resume')
def resume():
    return render_template('resume.html')

if __name__ == "__main__":
    app.debug = False
    app.run()