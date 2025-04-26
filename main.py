import tkinter as tk
from tkinter import ttk
import logging
from datetime import datetime
from splash_screen import SplashScreen
from login import LoginApp

# Configure logging
logging.basicConfig(
    filename=f'futuremt5_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FutureMT5:
    def __init__(self):
        """Initialize the main application."""
        try:
            # Set application-wide configurations
            self.setup_application()
            # Start with splash screen
            self.start_application()
        except Exception as e:
            logging.error(f"Application initialization error: {str(e)}")
            raise

    def setup_application(self):
        """Configure initial application settings."""
        # Set default theme configurations
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure modern looking theme
        self.style.configure(
            ".",
            background="#121212",
            foreground="white",
            fieldbackground="#1E1E1E",
            troughcolor="#2E2E2E",
            selectbackground="#3700B3",
            selectforeground="white"
        )
        
        # Configure specific styles
        self.style.configure(
            "TButton",
            padding=10,
            relief="flat",
            background="#BB86FC"
        )
        
        self.style.configure(
            "TEntry",
            padding=10,
            fieldbackground="#2E2E2E"
        )

    def start_application(self):
        """Initialize and start the application flow."""
        try:
            logging.info("Starting FutureMT5 application")
            self.root = tk.Tk()
            self.root.withdraw()  # Hide main window initially
            
            # Start with splash screen
            splash = SplashScreen(on_close=self.initialize_login)
            splash.mainloop()
        except Exception as e:
            logging.error(f"Error starting application: {str(e)}")
            raise

    def initialize_login(self):
        """Initialize the login window after splash screen."""
        try:
            logging.info("Initializing login window")
            self.root = tk.Tk()
            self.login = LoginApp(self.root)
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Login initialization error: {str(e)}")
            raise

def main():
    """Main entry point of the application."""
    try:
        app = FutureMT5()
    except Exception as e:
        logging.critical(f"Critical application error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
