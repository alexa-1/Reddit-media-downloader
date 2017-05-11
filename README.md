# Reddit-media-downloader
Downloads media from reddit links, including imgur, gfycat, direct links and reddit-hosted pages.

## NSFW Warning
This project was designed for NSFW/pornographic content. It contains the names of explicit subreddits.

## Screenshot
Here is the project in action.

![screenshot](https://raw.githubusercontent.com/alexa-1/Reddit-media-downloader/master/screenshot.png "Screenshot")

## Instructions
**Note**: This project requires **Python 2.7** to be installed. [Download here](https://www.python.org/downloads/)

1. Download [Reddit-media-downloader.py](https://raw.githubusercontent.com/alexa-1/Reddit-media-downloader/master/Reddit-media-downloader.py) - Right click > Save as...
2. Run the script by double-clicking it (Python 2.7 must be installed for this)
3. Type in a list of subreddits into the large textbox, or press 'Top NSFW subreddits' to populate it automatically
4. Enter your reddit username and password into the fields (this is required, otherwise Reddit blocks the requests)
5. Enter the number of pages you wish to download from in the categories of *Hot*, *Top of week*, *Top of month* or *Top of all time*
6. Press 'Download!' to start downloading - files will be downloaded to the same folder as the script

### Optional
- Tick 'Auto-open unhandled links' to automatically open unknown links (i.e. not imgur, gfycat, reddit etc.)
- Tick 'Auto-open text posts' to automatically open text/self posts

### Adding custom subreddits
You can add your own subreddits to be populated when pressing 'My subreddits'. To do this, open the python file in a text editor, and enter your favourite subreddits into the my_subreddits list (line 74).
