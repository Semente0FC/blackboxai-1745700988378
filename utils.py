import json
import os
import tkinter as tk
from tkinter import ttk
import ctypes
import platform

# Check if running on Windows
IS_WINDOWS = platform.system() == 'Windows'
import logging
import mt5_mock as mt5
from typing import Optional, Dict, List, Tuple
from pathlib import Path
from datetime import datetime
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    """Handle secure storage and retrieval of sensitive data."""
    
    def __init__(self):
        """Initialize security manager with encryption key."""
        self._key = self._generate_key()
        self._fernet = Fernet(self._key)

    def _generate_key(self) -> bytes:
        """Generate encryption key using system-specific data."""
        try:
            salt = b"FutureMT5_Salt"  # Constant salt
            # Use system info as password
            system_info = str(os.getlogin() + os.name).encode()
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(system_info))
            return key
        except Exception as e:
            logging.error(f"Key generation error: {str(e)}")
            return Fernet.generate_key()

    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data."""
        try:
            return self._fernet.encrypt(data.encode()).decode()
        except Exception as e:
            logging.error(f"Encryption error: {str(e)}")
            return ""

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        try:
            return self._fernet.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logging.error(f"Decryption error: {str(e)}")
            return ""

class LoginManager:
    """Manage MT5 login credentials."""
    
    def __init__(self):
        """Initialize login manager."""
        self.security = SecurityManager()
        self.credentials_file = "mt5_credentials.secure"

    def save_login(self, server: str, login: int, password: str) -> bool:
        """
        Save login credentials securely.
        
        Args:
            server: MT5 server address
            login: MT5 account number
            password: MT5 account password
            
        Returns:
            bool: True if saved successfully
        """
        try:
            data = {
                "server": server,
                "login": login,
                "password": self.security.encrypt(password)
            }
            
            with open(self.credentials_file, "w") as f:
                json.dump(data, f)
            
            return True
            
        except Exception as e:
            logging.error(f"Error saving credentials: {str(e)}")
            return False

    def load_login(self) -> Optional[Dict]:
        """
        Load saved login credentials.
        
        Returns:
            Optional[Dict]: Credentials if found, None otherwise
        """
        try:
            if not os.path.exists(self.credentials_file):
                return None
                
            with open(self.credentials_file, "r") as f:
                data = json.load(f)
                
            if "password" in data:
                data["password"] = self.security.decrypt(data["password"])
                
            return data
            
        except Exception as e:
            logging.error(f"Error loading credentials: {str(e)}")
            return None

class ThemeManager:
    """Manage application theming."""
    
    DARK_THEME = {
        "bg": "#121212",
        "fg": "white",
        "input_bg": "#2E2E2E",
        "card": "#1E1E1E",
        "primary": "#BB86FC",
        "secondary": "#03DAC6",
        "error": "#CF6679",
        "success": "#4CAF50"
    }
    
    LIGHT_THEME = {
        "bg": "#F5F5F5",
        "fg": "#121212",
        "input_bg": "#FFFFFF",
        "card": "#FFFFFF",
        "primary": "#6200EE",
        "secondary": "#03DAC6",
        "error": "#B00020",
        "success": "#4CAF50"
    }

    @classmethod
    def apply_theme(cls, root: tk.Tk, theme: str = "dark"):
        """
        Apply theme to application windows.
        
        Args:
            root: Root window
            theme: Theme name ("dark" or "light")
        """
        colors = cls.DARK_THEME if theme == "dark" else cls.LIGHT_THEME
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk styles
        style.configure(".", 
            background=colors["bg"],
            foreground=colors["fg"],
            fieldbackground=colors["input_bg"]
        )
        
        style.configure("TButton",
            padding=10,
            background=colors["primary"],
            foreground="white"
        )
        
        style.configure("TEntry",
            fieldbackground=colors["input_bg"],
            foreground=colors["fg"]
        )
        
        # Configure tk widgets
        for widget in cls._get_all_widgets(root):
            try:
                if isinstance(widget, (tk.Frame, tk.Label)):
                    widget.configure(
                        bg=colors["bg"],
                        fg=colors["fg"]
                    )
                elif isinstance(widget, tk.Entry):
                    widget.configure(
                        bg=colors["input_bg"],
                        fg=colors["fg"],
                        insertbackground=colors["fg"]
                    )
                elif isinstance(widget, tk.Button):
                    widget.configure(
                        bg=colors["primary"],
                        fg="white",
                        activebackground=colors["secondary"]
                    )
            except:
                pass

    @staticmethod
    def _get_all_widgets(widget):
        """Recursively get all child widgets."""
        children = widget.winfo_children()
        result = []
        for child in children:
            result.append(child)
            result.extend(ThemeManager._get_all_widgets(child))
        return result

class WindowManager:
    """Manage window appearance and behavior."""
    
    @staticmethod
    def center_window(window: tk.Tk, width: int, height: int):
        """
        Center window on screen.
        
        Args:
            window: Window to center
            width: Window width
            height: Window height
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def apply_modern_style(window: tk.Tk):
        """Apply modern window styling."""
        try:
            if IS_WINDOWS:
                # Enable DPI awareness
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)
                except:
                    pass

                # Set window attributes
                window.attributes('-alpha', 1.0)
                window.attributes('-topmost', True)
                
                # Modern window frame
                GWL_STYLE = -16
                WS_MINIMIZEBOX = 0x00020000
                WS_MAXIMIZEBOX = 0x00010000
                
                hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
                style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
                style = style & ~WS_MAXIMIZEBOX  # Remove maximize button
                ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            else:
                # Basic styling for non-Windows platforms
                window.attributes('-alpha', 1.0)
                window.attributes('-topmost', True)
            
        except Exception as e:
            logging.warning(f"Modern style application failed: {str(e)}")

class MT5Helper:
    """Helper functions for MetaTrader 5 operations."""
    
    @staticmethod
    def get_symbols() -> List[Tuple[str, str]]:
        """
        Get available trading symbols.
        
        Returns:
            List of tuples (symbol name, description)
        """
        try:
            symbols = []
            for symbol in mt5.symbols_get():
                if symbol.visible and symbol.ask > 0:
                    symbols.append((symbol.name, symbol.description))
            return symbols
        except Exception as e:
            logging.error(f"Error getting symbols: {str(e)}")
            return []

    @staticmethod
    def get_timeframes() -> Dict[str, int]:
        """
        Get available timeframes.
        
        Returns:
            Dictionary of timeframe names and values
        """
        return {
            "M1 (1 Minute)": mt5.TIMEFRAME_M1,
            "M5 (5 Minutes)": mt5.TIMEFRAME_M5,
            "M15 (15 Minutes)": mt5.TIMEFRAME_M15,
            "M30 (30 Minutes)": mt5.TIMEFRAME_M30,
            "H1 (1 Hour)": mt5.TIMEFRAME_H1,
            "H4 (4 Hours)": mt5.TIMEFRAME_H4,
            "D1 (Daily)": mt5.TIMEFRAME_D1
        }

    @staticmethod
    def format_price(price: float, digits: int = 5) -> str:
        """
        Format price with proper decimal places.
        
        Args:
            price: Price to format
            digits: Number of decimal places
            
        Returns:
            Formatted price string
        """
        return f"{price:.{digits}f}"

# Initialize logging
logging.basicConfig(
    filename=f'futuremt5_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create instances of managers
login_manager = LoginManager()
theme_manager = ThemeManager()
window_manager = WindowManager()
mt5_helper = MT5Helper()
