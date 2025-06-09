import os
import sys
import time
import subprocess

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

# Default config for NGINX RTMP module
defaultconfig = """\n
rtmp {
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

# Batch file content for Windows to start and stop the server
startbatch = r"""@echo off
cd C:\RTMPServer
start nginx.exe
echo Nginx RTMP server started.
pause
"""

stopbatch = r"""@echo off
cd C:\RTMPServer
nginx.exe -s stop
echo Nginx RTMP server stopped.
pause
"""

# Paths for Windows batch files on Desktop
user = os.environ.get("USERNAME")
startname = os.path.join("C:\\Users", user, "Desktop", "start.bat")
stopname = os.path.join("C:\\Users", user, "Desktop", "stop.bat")

# Debian package dependencies
debianpkgs = "build-essential libpcre3 libpcre3-dev libssl-dev wget unzip git"

def print_banner():
    print(BLUE + LOGO + RESET)

def create_batch_files():
    print(GREEN + "[INFO] Creating batch files on your Desktop..." + RESET)
    try:
        with open(startname, "w") as f:
            f.write(startbatch)
        with open(stopname, "w") as f:
            f.write(stopbatch)
        print(GREEN + f"[INFO] Batch files created:\n  {startname}\n  {stopname}" + RESET)
    except Exception as e:
        print(RED + f"[ERROR] Failed to create batch files: {e}" + RESET)

def run_command(command, check=True, shell=False):
    """Helper to run shell commands and print output."""
    print(YELLOW + f"[CMD] {command}" + RESET)
    try:
        subprocess.run(command, check=check, shell=shell)
    except subprocess.CalledProcessError as e:
        print(RED + f"[ERROR] Command failed: {e}" + RESET)
        sys.exit(1)

# Windows Download and Setup
def download_win():
    print(YELLOW + "[INFO] Setting up nginx-rtmp-win32 on Windows..." + RESET)

    # Create directory C:\RTMPServer
    rtmp_dir = "C:\\RTMPServer"
    if not os.path.exists(rtmp_dir):
        os.makedirs(rtmp_dir)

    # Clone the repo if not already cloned
    if not os.path.exists(os.path.join(rtmp_dir, ".git")):
        run_command(["git", "clone", "https://github.com/illuspas/nginx-rtmp-win32.git", rtmp_dir])
    else:
        print(GREEN + "[INFO] RTMPServer directory already exists, skipping git clone." + RESET)

    print(GREEN + "[INFO] RTMPServer installed!" + RESET)

    choice = input("Do you want batch files on your Desktop to start/stop the Nginx server? [yes/no]: ").strip().lower()
    if choice == "yes":
        create_batch_files()
    else:
        print("No batch files created.")

# Linux (Debian-based) Download and Setup
def download_posix():
    print(YELLOW + "[INFO] Updating package manager and installing dependencies..." + RESET)
    run_command(["sudo", "apt", "update"])
    run_command(["sudo", "apt", "install", "-y"] + debianpkgs.split())

    # Download sources
    print(YELLOW + "[INFO] Downloading nginx and nginx-rtmp-module sources..." + RESET)
    run_command(["wget", "http://nginx.org/download/nginx-1.15.1.tar.gz"])
    run_command(["wget", "https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/dev.zip"])

    # Extract archives
    run_command(["tar", "-zxvf", "nginx-1.15.1.tar.gz"])
    run_command(["unzip", "dev.zip"])

    # Build nginx with rtmp module
    os.chdir("nginx-1.15.1")
    print(YELLOW + "[INFO] Configuring nginx with RTMP module..." + RESET)
    run_command(["./configure", "--with-http_ssl_module", "--add-module=../nginx-rtmp-module-dev"])
    run_command(["make"])
    run_command(["sudo", "make", "install"])

    # Append default RTMP config
    nginx_conf_path = "/usr/local/nginx/conf/nginx.conf"
    try:
        with open(nginx_conf_path, "a") as f:
            f.write(defaultconfig)
        print(GREEN + f"[INFO] RTMP config appended to {nginx_conf_path}" + RESET)
    except Exception as e:
        print(RED + f"[ERROR] Failed to append RTMP config: {e}" + RESET)

    print(GREEN + "[INFO] Installed RTMPServer!" + RESET)
    print("Start with: sudo /usr/local/nginx/sbin/nginx")
    print("Stop with: sudo /usr/local/nginx/sbin/nginx -s stop")
    print("Server is configured to run on http://localhost")

    print("Closing in 5 seconds...")
    time.sleep(5)

def start_installation():
    print_banner()
    
    if os.name == "nt":
        print(GREEN + "[INFO] Windows system detected." + RESET)
        download_win()
    elif os.name == "posix":
        print(GREEN + "[INFO] Linux (Debian-based) system detected." + RESET)
        print("This script currently supports Debian or Debian-based distributions.")
        choice = input("Do you want to continue? [yes/no]: ").strip().lower()
        if choice == "yes":
            download_posix()
        else:
            print("Exiting...")
            sys.exit()
    else:
        print(RED + "[ERROR] Unsupported OS!" + RESET)
        sys.exit()

if __name__ == "__main__":
    start_installation()
