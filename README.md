# RTMPServer
An open-source server and installer for hosting rtmp server with nginx
### Note: Currently, this script only work and tested on Windows 7+, it may not work in linux or other oses

# Requirements
- Python 3 or higher
- git [download for windows here](https://git-scm.com/downloads)
- working brain
  
# Tested
- Windows 10 Server 2022

# Not Tested
- Windows 10/11
- Linux
- Android and IOS

# How to use it
- After installing RTMPServer, run start.bat script or run nginx.exe
- after that open a streaming software that support rtmp (exemple: obs studio)
- set stream url to rtmp://localhost/live and set stream key to anything you want
- start the stream
- if you want to play the stream, make sure you have a player that support RTMP (exemple: VLC)
- play rtmp://localhost:8080/live/(stream key)
- and here we go, it should work 
- if it doesnt work, Please report to issues
- It may not work in first time, just keep trying
