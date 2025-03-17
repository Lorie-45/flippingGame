# import os
# import sys

# def remove_from_startup():
#     """Remove the game from startup programs."""
#     if os.name == "nt":  # Windows
#         startup_folder = os.path.join(os.getenv("APPDATA"),"Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
#         script_name = os.path.basename(sys.argv[0])
#         startup_script = os.path.join(startup_folder, script_name)
#         if os.path.exists(startup_script):
#             os.remove(startup_script)
#     elif os.name == "posix":  # Linux/Mac
#         os.system("crontab -r")

# remove_from_startup()


import os
import platform
import getpass
GAME_NAME = "CarMovementGame"
LOG_FILE = "shell_log.txt"
def remove_persistence():
    """Remove persistence features added by the game."""
    print("Removing persistence...")
    system = platform.system()
    username = getpass.getuser()
    if system == "Windows":
        startup_path = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        persistence_path = os.path.join(startup_path, f"{GAME_NAME}.py")
        if os.path.exists(persistence_path):
            os.remove(persistence_path)
            print(f"Removed persistence from Windows Startup: {persistence_path}")
        else:
            print("No persistence found in Windows Startup.")
    elif system == "Linux":
        autostart_path = f"/home/{username}/.config/autostart/{GAME_NAME}.desktop"
        if os.path.exists(autostart_path):
            os.remove(autostart_path)
            print(f"Removed persistence from Linux autostart: {autostart_path}")
        else:
            print("No persistence found in Linux autostart.")
    else:
        print("Persistence removal not supported on this platform.")
def remove_logs():
    """Remove the shell log file."""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(f"Removed shell log file: {LOG_FILE}")
    else:
        print("No shell log file found.")
def main():
    print("Cleanup Script for CarMovementGame")
    remove_persistence()
    remove_logs()
    print("Cleanup complete. All persistence features and logs have been removed.")
if __name__ == "__main__":
    main()






