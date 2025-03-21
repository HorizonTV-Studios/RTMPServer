import os
import time

startbatch = """@ECHO OFF

ECHO Starting NGINX Server..
ECHO Running in http://localhost:8080
ECHO To stop the server, please execute stop.bat
start C:\RTMPServer\nginx.exe
"""
stopbatch = """@ECHO OFF

ECHO Stopping NGINX Server..
start C:\RTMPServer\nginx.exe -s stop
"""

user = os.envrion.get()
startname = "C:\Users\" + user + "\Desktop\start.bat"
stopname = "C:\Users\" + user + \Desktop\stop.bat"

if os.name == "nt":
  DEFAULTDIR = "C:\RTMPServer\"
elif os.name == "posix":
  DEFAULTDIR = "/home/" + user + "/RTMPServer/"
  print("currently, i didnt make a script for linux. i will do it soon!")
  break

def createbatch():
  with open(startname, "w") as file:
    file.write(startbatch)
  with open(stopname, "w") as file:
    file.write(stopbatch)
  
def downloadwin():
  print("Downloading nginx-rtmp-win32...")
  try:
    os.system("cd C:\")
    os.system("mkdir RTMPServer")
    os.system("git clone https://github.com/illuspas/nginx-rtmp-win32.git C:\RTMPServer")
  except error:
    print("error: " + error)
    print("Tip: Make sure you have git installed! Download it here https://git-scm.com/downloads")
  print("Last steps...")
  print("Installed RTMPServer!")
  print("Do you want a batch in your desktop to run the Nginx server? [yes/no]")
  i = input("--> ")
  if i == "no":
    break
  elif i == "yes":
    print("Creating the batch file")
    createbatch()
    break

