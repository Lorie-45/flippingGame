import os
import subprocess

# List of required dependencies
required_dependencies = ["pygame"]

def check_and_install_dependencies():
    for dependency in required_dependencies:
        try:
            __import__(dependency)
            print(f"{dependency} is already installed.")
        except ImportError:
            print(f"{dependency} is not installed. Installing...")
            subprocess.check_call(["pip", "install", dependency])

# Run the check before starting the game
check_and_install_dependencies()