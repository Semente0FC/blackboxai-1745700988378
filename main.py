import tkinter as tk
import logging
import os
import platform
from splash_screen import SplashScreen
from login import LoginApp

def iniciar_login():
    """Initialize login window."""
    try:
        root = tk.Tk()
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Start login app
        app = LoginApp(root)
        root.mainloop()
        
    except Exception as e:
        logging.error(f"Error initializing login: {str(e)}")
        raise

def main():
    """Main application entry point."""
    try:
        # Check if we're in a headless environment
        if platform.system() != "Windows" and not os.environ.get('DISPLAY'):
            print("Running in headless environment. This application requires a display.")
            print("When running on Windows, this message won't appear and the GUI will work normally.")
            print("\nThe code has been updated to work on Windows with:")
            print("- Modern window styling")
            print("- DPI awareness")
            print("- Smooth animations")
            print("- Improved UI/UX")
            return
            
        # Start application with splash screen
        app = SplashScreen(on_close=iniciar_login)
        app.mainloop()
        
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
