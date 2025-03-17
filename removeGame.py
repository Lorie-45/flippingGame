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
import sys
import platform
import subprocess

def remove_from_startup():
    """Remove main.exe from startup with clear status messages."""
    if os.name == "nt":
        # Windows: Target main.exe and its potential shortcut
        startup_folder = os.path.join(
            os.getenv("APPDATA"),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )
        
        # Explicitly set to your executable name
        script_name = "main.exe"
        shortcut_name = "main.lnk"  # Directly set shortcut name
        
        target_path = os.path.join(startup_folder, script_name)
        shortcut_path = os.path.join(startup_folder, shortcut_name)

        removed = False
        for path, desc in [(target_path, "executable"), (shortcut_path, "shortcut")]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"✅ Successfully removed {desc}: {os.path.basename(path)}")
                    removed = True
                except Exception as e:
                    print(f"❌ Failed to remove {desc} ({os.path.basename(path)}): {str(e)}")
            else:
                print(f"ℹ️ No {desc} found: {os.path.basename(path)}")

        if not removed:
            print("⚠️ main.exe was not found in Windows startup locations")

    elif os.name == "posix":
        if platform.system() == "Linux":
            # Linux: Remove cron job for main.exe
            try:
                cron_out = subprocess.check_output(["crontab", "-l"], 
                                                stderr=subprocess.DEVNULL).decode()
            except subprocess.CalledProcessError:
                print("ℹ️ No cron jobs found for main.exe")
                return

            # Look for cron entries containing "main.exe"
            new_cron = "\n".join(
                line for line in cron_out.splitlines()
                if "main.exe" not in line
            )

            if cron_out == new_cron:
                print("ℹ️ No main.exe cron jobs found")
                return

            try:
                subprocess.run(["crontab", "-"], input=new_cron.encode(), check=True)
                print("✅ Successfully removed main.exe from cron jobs")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to update crontab for main.exe: {str(e)}")

        elif platform.system() == "Darwin":
            # macOS: Custom launch agent for main.exe
            plist_name = "com.user.main.plist"  # Descriptive name for your app
            plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{plist_name}")
            
            if os.path.exists(plist_path):
                try:
                    subprocess.run(["launchctl", "unload", plist_path], check=True)
                    os.remove(plist_path)
                    print(f"✅ Successfully removed main.exe launch agent: {plist_name}")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to unload main.exe agent: {str(e)}")
                except Exception as e:
                    print(f"❌ Error removing main.exe plist: {str(e)}")
            else:
                print(f"ℹ️ No launch agent found for main.exe: {plist_name}")

remove_from_startup()