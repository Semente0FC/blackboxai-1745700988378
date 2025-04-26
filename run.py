import os
import subprocess
import time
from threading import Thread

def start_xvfb():
    """Start Xvfb display server."""
    # Kill any existing Xvfb processes
    subprocess.run("pkill Xvfb", shell=True)
    time.sleep(1)
    
    # Start Xvfb
    subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1024x768x24"])
    time.sleep(2)  # Wait for Xvfb to start

def main():
    """Main entry point."""
    # Start Xvfb
    start_xvfb()
    
    # Set display
    os.environ["DISPLAY"] = ":99"
    
    # Run the application
    import main
    main.main()

if __name__ == "__main__":
    main()
