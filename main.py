import tkinter as tk
import os
import subprocess
import time
import logging
from splash_screen import SplashScreen
from login import LoginApp

def setup_display():
    """Set up virtual display for headless environment."""
    try:
        # Kill any existing Xvfb processes
        subprocess.run(['pkill', 'Xvfb'], stderr=subprocess.DEVNULL)
        time.sleep(1)
        
        # Start Xvfb with specific options for better stability
        display_num = 99
        subprocess.Popen([
            'Xvfb', 
            f':{display_num}', 
            '-screen', '0', '1024x768x24',
            '-ac',  # Disable access control
            '+extension', 'RANDR',
            '+render',
            '-noreset'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(2)  # Wait for Xvfb to start
        
        # Set display
        os.environ['DISPLAY'] = f':{display_num}'
        
    except Exception as e:
        logging.error(f"Error setting up display: {e}")
        raise

def iniciar_login():
    """Initialize login window."""
    try:
        root = tk.Tk()
        root.withdraw()  # Hide root window initially
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Start login app
        app = LoginApp(root)
        root.deiconify()  # Show window
        root.mainloop()
        
    except Exception as e:
        logging.error(f"Error initializing login: {e}")
        raise

def main():
    """Main application entry point."""
    try:
        # Set up display for headless environment
        setup_display()
        
        # Start application with splash screen
        root = tk.Tk()
        root.withdraw()  # Hide root window
        
        app = SplashScreen(on_close=iniciar_login)
        app.mainloop()
        
    except Exception as e:
        logging.error(f"Application error: {e}")
        raise
    finally:
        # Cleanup
        try:
            subprocess.run(['pkill', 'Xvfb'], stderr=subprocess.DEVNULL)
        except:
            pass

if __name__ == "__main__":
    main()
