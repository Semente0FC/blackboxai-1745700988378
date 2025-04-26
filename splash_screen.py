import tkinter as tk
import threading
import time
import logging
from typing import Callable
import ctypes

class SplashScreen(tk.Tk):
    """
    Modern splash screen with smooth animations and loading indicators.
    """
    
    def __init__(self, on_close: Callable[[], None]):
        """
        Initialize splash screen with modern design and animations.
        
        Args:
            on_close: Callback function to execute when splash screen closes
        """
        super().__init__()
        
        # Initialize properties
        self.on_close = on_close
        self.alpha = 0.0
        
        # Configure window
        self.setup_window()
        
        # Create UI elements
        self.create_ui_elements()
        
        # Start animations
        self.start_animations()
        
        logging.info("Splash screen initialized")

    def setup_window(self):
        """Configure the main window properties."""
        # Window setup
        self.title("Future MT5")
        self.geometry("600x300")
        self.configure(bg="#121212")
        self.overrideredirect(True)
        self.center_window()
        self.attributes('-alpha', self.alpha)
        
        # Apply modern styling
        self.apply_modern_style()

    def create_ui_elements(self):
        """Create and arrange UI elements."""
        # Main container
        self.container = tk.Frame(self, bg="#121212")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Logo frame
        logo_frame = tk.Frame(self.container, bg="#121212")
        logo_frame.pack(expand=True)
        
        # Rocket emoji with glow effect
        self.logo = tk.Label(
            logo_frame,
            text="🚀",
            font=("Helvetica", 48),
            bg="#121212",
            fg="white"
        )
        self.logo.pack()
        
        # Title with modern font
        self.title_label = tk.Label(
            logo_frame,
            text="FUTURE MT5",
            font=("Helvetica", 24, "bold"),
            bg="#121212",
            fg="#BB86FC"
        )
        self.title_label.pack(pady=(10, 5))
        
        # Subtitle
        self.subtitle = tk.Label(
            logo_frame,
            text="Trading Automation Platform",
            font=("Helvetica", 12),
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
        """Start all animations in separate threads."""
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
                    self.logo.configure(font=("Helvetica", size))
                    time.sleep(0.05)
                
                # Decrease size
                for size in range(52, 48, -1):
                    self.logo.configure(font=("Helvetica", size))
                    time.sleep(0.05)
                    
        except Exception as e:
            logging.error(f"Logo animation error: {str(e)}")

    def close_splash(self):
        """Close splash screen and call the callback function."""
        try:
            # Fade out effect
            for i in range(10, -1, -1):
                self.alpha = i / 10
                self.attributes('-alpha', self.alpha)
                time.sleep(0.05)
            
            self.destroy()
            self.on_close()
            
        except Exception as e:
            logging.error(f"Error closing splash screen: {str(e)}")

    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def apply_modern_style(self):
        """Apply modern window styling with rounded corners."""
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            
            class MARGINS(ctypes.Structure):
                _fields_ = [
                    ("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int)
                ]
            
            margins = MARGINS(2, 2, 2, 2)
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
            
        except Exception as e:
            logging.warning(f"Failed to apply modern window style: {str(e)}")

if __name__ == "__main__":
    # Test splash screen
    def on_close_callback():
        print("Splash screen closed")
    
    app = SplashScreen(on_close=on_close_callback)
    app.mainloop()
