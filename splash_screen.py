import tkinter as tk
import threading
import time
import logging
from typing import Callable
import ctypes
import platform

# Check if running on Windows
IS_WINDOWS = platform.system() == 'Windows'

class SplashScreen(tk.Tk):
    """Modern splash screen with smooth animations."""
    
    def __init__(self, on_close: Callable[[], None]):
        """Initialize splash screen."""
        super().__init__()
        self.on_close = on_close
        self.alpha = 0.0  # Store alpha value
        
        # Set DPI awareness for Windows
        if IS_WINDOWS:
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        self.setup_window()
        self.create_ui()
        self.start_animations()
        
        logging.info("Splash screen initialized")

    def setup_window(self):
        """Configure the main window."""
        self.title("Future MT5")
        self.geometry("600x300")
        self.configure(bg="#121212")
        self.overrideredirect(True)  # Borderless window
        self.center_window()
        self.attributes('-alpha', self.alpha)
        
        # Window styling
        self.attributes('-topmost', True)  # Keep on top
        if IS_WINDOWS:
            self.attributes('-toolwindow', True)  # No taskbar icon on Windows

    def create_ui(self):
        """Create user interface elements."""
        # Main container
        self.container = tk.Frame(self, bg="#121212")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Logo frame
        logo_frame = tk.Frame(self.container, bg="#121212")
        logo_frame.pack(expand=True)
        
        # Rocket emoji with glow effect
        font_family = "Segoe UI" if IS_WINDOWS else "Helvetica"
        self.logo = tk.Label(
            logo_frame,
            text="🚀",
            font=(font_family, 48),
            bg="#121212",
            fg="white"
        )
        self.logo.pack()
        
        # Title with modern font
        self.title_label = tk.Label(
            logo_frame,
            text="FUTURE MT5",
            font=(font_family, 24, "bold"),
            bg="#121212",
            fg="#BB86FC"
        )
        self.title_label.pack(pady=(10, 5))
        
        # Subtitle
        self.subtitle = tk.Label(
            logo_frame,
            text="Trading Automation Platform",
            font=(font_family, 12),
            bg="#121212",
            fg="#03DAC6"
        )
        self.subtitle.pack()
        
        # Loading bar
        self.progress_frame = tk.Frame(
            self.container,
            bg="#121212",
            height=2
        )
        self.progress_frame.pack(fill=tk.X, padx=50, pady=(20, 30))
        
        self.progress_bar = tk.Canvas(
            self.progress_frame,
            height=2,
            bg="#121212",
            highlightthickness=0
        )
        self.progress_bar.pack(fill=tk.X)
        
        # Create loading bar animation
        self.progress_line = self.progress_bar.create_line(
            0, 1, 0, 1,
            fill="#BB86FC",
            width=2
        )

    def start_animations(self):
        """Start all animations."""
        # Start fade-in animation
        threading.Thread(target=self.animate_fade_in, daemon=True).start()
        
        # Start loading bar animation
        threading.Thread(target=self.animate_loading_bar, daemon=True).start()
        
        # Start logo pulse animation
        threading.Thread(target=self.animate_logo_pulse, daemon=True).start()

    def animate_fade_in(self):
        """Animate window fade-in effect."""
        try:
            for i in range(0, 11):
                self.alpha = i / 10
                self.attributes('-alpha', self.alpha)
                time.sleep(0.05)
            
            # Schedule close after animations
            self.after(2000, self.close_splash)
            
        except Exception as e:
            logging.error(f"Fade-in animation error: {str(e)}")

    def animate_loading_bar(self):
        """Animate loading bar progress."""
        try:
            width = self.progress_bar.winfo_reqwidth()
            for i in range(width + 1):
                self.progress_bar.coords(
                    self.progress_line,
                    0, 1, i, 1
                )
                time.sleep(2/width)  # Adjust speed based on width
                
        except Exception as e:
            logging.error(f"Loading bar animation error: {str(e)}")

    def animate_logo_pulse(self):
        """Animate logo pulsing effect."""
        try:
            while True:
                # Increase size
                for size in range(48, 52, 1):
                    self.logo.configure(font=(self.logo.cget("font").split()[0], size))
                    time.sleep(0.05)
                
                # Decrease size
                for size in range(52, 48, -1):
                    self.logo.configure(font=(self.logo.cget("font").split()[0], size))
                    time.sleep(0.05)
                    
        except Exception as e:
            logging.error(f"Logo animation error: {str(e)}")

    def close_splash(self):
        """Close splash screen with fade-out effect."""
        try:
            # Fade out
            for i in range(10, -1, -1):
                self.alpha = i / 10
                self.attributes('-alpha', self.alpha)
                time.sleep(0.05)
                
            self.destroy()
            self.on_close()
            
        except Exception as e:
            logging.error(f"Error closing splash screen: {str(e)}")

    def center_window(self):
        """Center window on screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    # Test splash screen
    def on_close_callback():
        print("Splash screen closed")
    
    app = SplashScreen(on_close=on_close_callback)
    app.mainloop()
