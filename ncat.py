import os
import subprocess
import platform
import sys

def check_and_install_ncat():
    """Check if ncat is installed, and install it if missing."""
    try:
        # Check if ncat is installed
        subprocess.run(["ncat", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ncat is already installed.")
    except FileNotFoundError:
        print("ncat is not installed. Installing...")
        if platform.system() == "Windows":
            # Download ncat for Windows
            ncat_url = "https://nmap.org/dist/nmap-7.92-win32.zip"
            try:
                # Download the Nmap package
                subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {ncat_url} -OutFile ncat.zip"], check=True)
                # Extract the package
                subprocess.run(["powershell", "-Command", "Expand-Archive -Path ncat.zip -DestinationPath ."], check=True)
                # Add ncat to the system PATH
                os.environ["PATH"] += os.pathsep + os.path.abspath("nmap-7.92")
                print("ncat has been installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install ncat: {e}")
                sys.exit(1)
        elif platform.system() == "Linux":
            # Install ncat using package manager
            try:
                subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
                print("ncat has been installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install ncat: {e}")
                sys.exit(1)
        elif platform.system() == "Darwin":  # macOS
            # Install ncat using Homebrew
            try:
                subprocess.run(["brew", "install", "nmap"], check=True)
                print("ncat has been installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install ncat: {e}")
                sys.exit(1)
        else:
            print("Unsupported operating system.")
            sys.exit(1)

# Main execution
if __name__ == "__main__":
    check_and_install_ncat()