# multi-channel-youtube-search
 Simple flask based webapp that'll let you search multiple specific YT channels for content. 

Disclaimer: 

  There is no intent of commercializing or undergoing any form of monetization in the making of this small webapp.
  This webapp is for educational and showcasing of current skills/concept purposes only.

Also some FYI:
  
  This repo is for showcase purposes only. 
  The project is already 'finished' aka in an acceptable state with no major issues or features to be addressed.
  There certainly are still improvements to be done but will not be undertaken at this time. 
  If you've stumbled upon here randomly, of course feedback is welcome, and also just some looking around.
  I know you see by now how amateur all this is because I still am just an amateur. 
  
  end product here: http://bluestreak.pythonanywhere.com/
  
About the project:
 
 Abstract:
   
   I am currently trying to pursue programming, and to brush up on my rusted skills I wanted to start some small project. 
   What I also am is an avid Youtube user. I encountered times when I want to look up certain content from multiple channels and found it tedious.
   One example of this is looking up the recent Steam Deck reviews that were uploaded ONLY by tech channels I specifically seek.
   With current Youtube features, I can only go to each channel one by one and search within the channel for 'Steam Deck'.
   A more compelling use case is when looking up streamed content from streamers, specifically V-Tubers. (which is one of my go-to entertainment)
   I load up pages of specific V-Tuber channels one by one and search 'GTA V' just to find out which of these channels I specifically wanted to search for have streamed GTA V in the past. There are tons of V-Tuber channels out there and I simply can't rely on default Youtube search function.

 How I decided to tackle the problem:
   
   Webscraping Youtube itself. 
   Through a webapp, utilize already existing search functions of Youtube and simplifying the process of searching multiple specific channels.
   End product will be deployed an a free hosting webapp service - in this case pythonanywhere.com

 Language used rationale:
   
   Python - I've been familiar with it and wanted to have some reengagement with it. Also webscraping and Python are well known together.
   HTML & CSS - Yes. I've also long forgotten how all these worked, and to be honest I re-studied a lot more here than I did with Python, as a result the project moved slower when working the front end. 

 Current known issues:
   
   Selected channels is only limited to 3 channels due to server limitions of the free hosting service.
   Despite channel limit, there will be times when an internal server error due to overloading will occur when searching certain channels for certain type of content (user video query).
   I currently don't have enough skills / knowledge to address this beyond limiting video search output to a certain amount (currently set to 5 videos max output) where the error still occurs despite applying this 'workaround'.
 

