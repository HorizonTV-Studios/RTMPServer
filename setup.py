import os
import time
import sys

# Themed colors for cool output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# ASCII Logo
LOGO = """
   _____ _____ _____ _____ 
  |     |  |  |   __|   __|
  |  |  |  |  |   __|__   |
  |_____|_____|_____|_____|
       Horizon TV Studios
"""

# Default config for NGINX
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

# Paths for Windows
user = os.environ.get("USERNAME")
startname = f"C:\\Users\\{user}\\Desktop\\start.bat"
stopname = f"C:\\Users\\{user}\\Desktop\\stop.bat"

# Debian package dependencies
debianpkgs = "build-essential libpcre3 libpcre3-dev libssl-dev wget"  # Add any missing packages here

def print_banner():
    print(BLUE + LOGO + RESET)

def create_batch_files():
    print(GREEN + "[INFO] Creating batch files..." + RESET)
    try:
        with open(startname, "w") as file:
            file.write(startbatch)
        with open(stopname, "w") as file:
            file.write(stopbatch)
        print(GREEN + "[INFO] Batch files created on your Desktop!" + RESET)
    except Exception as e:
        print(RED + f"[ERROR] Failed to create batch files: {e}" + RESET)

# Windows Download and Setup
def download_win():
    print(YELLOW + "[INFO] Downloading nginx-rtmp-win32..." + RESET)
    try:
        os.system("cd C:\\")
        os.system("mkdir RTMPServer")
        os.system("git clone https://github.com/illuspas/nginx-rtmp-win32.git C:\\RTMPServer")
    except Exception as error:
        print(RED + f"[ERROR] {error}" + RESET)
        print(YELLOW + "Tip: Make sure you have git installed! Download it here: https://git-scm.com/downloads" + RESET)
        return

    print(GREEN + "[INFO] Last steps..." + RESET)
    print(GREEN + "[INFO] Installed RTMPServer!" + RESET)
    print("Do you want a batch file on your Desktop to run the Nginx server? [yes/no]")

    i = input("--> ")
    if i.lower() == "yes":
        create_batch_files()
    else:
        print("No batch file created.")

# Linux (Debian-based) Download and Setup
def download_posix():
    print(YELLOW + "[INFO] Updating package manager..." + RESET)
    try:
        os.system("sudo apt update")
        os.system(f"sudo apt install {debianpkgs}")
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

        print(GREEN + "[INFO] Installed RTMPServer!" + RESET)
        print("Start with: sudo /usr/local/nginx/sbin/nginx")
        print("Stop with: sudo /usr/local/nginx/sbin/nginx -s stop")
        print("Server is configured to run on http://localhost")
    except Exception as error:
        print(RED + f"[ERROR] {error}" + RESET)
        print(YELLOW + "Make sure you have all the needed packages installed." + RESET)

    print("Closing in 5 seconds...")
    time.sleep(5)

# Start the installation process
def start_installation():
    print_banner()
    
    if os.name == "nt":
        print(GREEN + "[INFO] Windows system detected." + RESET)
        download_win()
    elif os.name == "posix":
        print(GREEN + "[INFO] Linux (Debian-based) system detected." + RESET)
        print("This script currently works for Debian or Debian-based distributions.")
        print("Do you want to continue? [yes/no]")
        
        choice = input("--> ")
        if choice.lower() == "yes":
            download_posix()
        else:
            print("Exiting...")
            sys.exit()
    else:
        print(RED + "[ERROR] Unsupported OS!" + RESET)
        sys.exit()

if __name__ == "__main__":
    start_installation()
