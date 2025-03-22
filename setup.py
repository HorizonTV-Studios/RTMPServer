import os
import time

startbatch = """@ECHO OFF

ECHO Starting NGINX Server..
ECHO Running in http://localhost:8080
ECHO To stop the server, please execute stop.bat
start C:\\RTMPServer\\nginx.exe
"""
stopbatch = """@ECHO OFF

ECHO Stopping NGINX Server..
start C:\\RTMPServer\\nginx.exe -s stop
"""

defaultconfig = """rtmp {
        server {
                listen 1935;
                chunk_size 4096;

                application live {
                        live on;
                        record off;
                }
        }
}
"""
user = os.environ.get("USERNAME")
startname = "C:\\Users\\" + user + "\\Desktop\\start.bat"
stopname = "C:\\Users\\" + user + "\\Desktop\\stop.bat"

debianpkgs = "build-essential libpcre3 libpcre3-dev libssl-dev wget" # Please pull a request if something wrong here


  

def createbatch():
  with open(startname, "w") as file:
    file.write(startbatch)
  with open(stopname, "w") as file:
    file.write(stopbatch)
  
def downloadwin():
  print("Downloading nginx-rtmp-win32...")
  try:
    os.system("cd C:\\")
    os.system("mkdir RTMPServer")
    os.system("git clone https://github.com/illuspas/nginx-rtmp-win32.git C:\\RTMPServer")
  except error:
    print("error: " + error)
    print("Tip: Make sure you have git installed! Download it here https://git-scm.com/downloads")
  print("Last steps...")
  print("Installed RTMPServer!")
  print("Do you want a batch in your desktop to run the Nginx server? [yes/no]")
  i = input("--> ")
  if i == "no":
    print("ok")
  elif i == "yes":
    print("Creating the batch file")
    createbatch()

def downloadposix():
  # only debian or based for now
  print("Updating package manager...")
  try:
   os.system("sudo apt update")
   os.system("sudo apt install " + debianpkgs) 
   os.system("wget http://nginx.org/download/nginx-1.15.1.tar.gz")
   os.system("wget https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/dev.zip")
   os.system("tar -zxvf nginx-1.15.1.tar.gz")
   os.system("unzip dev.zip")
   os.system("cd nginx-1.15.1")
   os.system("./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-dev")
   os.system("make")
   os.system("sudo make install")
   with open("/usr/local/nginx/conf/nginx.conf", "a") as file:
    file.write(defaultconfig)
  except error:
   print("error: " + error)
   print("make sure you have all needed packages installed")
  print("Installed RTMPServer!")
  print("start with sudo /usr/local/nginx/sbin/nginx")
  print("stop with sudo /usr/local/nginx/sbin/nginx -s stop")
  print("server is configured to be running on http://localhost")
  print("Closing in 5 seconds..")
  time.sleep(5)
  
if os.name == "nt":
  DEFAULTDIR = "C:\\RTMPServer\\"
  downloadwin()
elif os.name == "posix":
  DEFAULTDIR = "/home/" + user + "/RTMPServer/"
  print("only works in debian or debian based? because it uses APT Package manager..")
  print("this may not working correctly, do you want to continue? [yes/no]")
  j = input("--> ")
  if j == "yes":
   downloadposix()
  elif j == "no":
   print("ok")
    
