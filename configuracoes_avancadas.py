import tkinter as tk
from tkinter import ttk, messagebox
import json
import logging
from typing import Dict, Any
from pathlib import Path
from utils import ThemeManager, WindowManager

class ConfigurationManager:
    """Manage trading configuration settings."""
    
    DEFAULT_CONFIG = {
        "break_even": {
            "enabled": True,
            "pips": 15,
            "offset": 2
        },
        "trailing_stop": {
            "enabled": True,
            "start_pips": 25,
            "distance_pips": 10
        },
        "risk_management": {
            "daily_target": 3.0,
            "stop_on_target": True
        }
    }
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_file = Path("trading_config.json")
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r") as f:
                    return json.load(f)
            return self.DEFAULT_CONFIG
        except Exception as e:
            logging.error(f"Error loading config: {str(e)}")
            return self.DEFAULT_CONFIG
            
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Error saving config: {str(e)}")
            return False

class AdvancedSettingsWindow:
    """Advanced settings configuration window."""
    
    def __init__(self, parent: tk.Tk):
        """Initialize settings window."""
        self.parent = parent
        self.config_manager = ConfigurationManager()
        self.create_window()
        
    def create_window(self):
        """Create and setup the settings window."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Advanced Settings - Future MT5")
        self.window.geometry("600x700")
        WindowManager.center_window(self.window, 600, 700)
        self.window.resizable(False, False)
        WindowManager.apply_modern_style(self.window)
        
        # Get theme from parent
        self.current_theme = "dark" if self.parent.cget("bg") == "#121212" else "light"
        ThemeManager.apply_theme(self.window, self.current_theme)
        
        self.create_ui()
        
    def create_ui(self):
        """Create user interface elements."""
        # Main container
        self.container = ttk.Frame(self.window)
        self.container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title
        self.create_header()
        
        # Settings sections
        self.create_break_even_section()
        self.create_trailing_stop_section()
        self.create_risk_management_section()
        
        # Buttons
        self.create_action_buttons()
        
    def create_header(self):
        """Create header section."""
        header_frame = ttk.Frame(self.container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(
            header_frame,
            text="⚙️ Advanced Trading Settings",
            font=("Helvetica", 16, "bold")
        )
        title.pack()
        
        description = ttk.Label(
            header_frame,
            text="Configure advanced trading parameters",
            font=("Helvetica", 10)
        )
        description.pack()
        
    def create_break_even_section(self):
        """Create break-even settings section."""
        section = self.create_section_frame("Break Even Settings")
        
        # Enable/Disable
        self.be_enabled = tk.BooleanVar(
            value=self.config_manager.config["break_even"]["enabled"]
        )
        ttk.Checkbutton(
            section,
            text="Enable Break Even",
            variable=self.be_enabled
        ).pack(anchor="w", pady=5)
        
        # Pips settings
        pips_frame = ttk.Frame(section)
        pips_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pips_frame, text="Activation (pips):").pack(side=tk.LEFT)
        self.be_pips = ttk.Entry(pips_frame, width=10)
        self.be_pips.insert(0, str(self.config_manager.config["break_even"]["pips"]))
        self.be_pips.pack(side=tk.RIGHT)
        
        # Offset settings
        offset_frame = ttk.Frame(section)
        offset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(offset_frame, text="Offset (pips):").pack(side=tk.LEFT)
        self.be_offset = ttk.Entry(offset_frame, width=10)
        self.be_offset.insert(0, str(self.config_manager.config["break_even"]["offset"]))
        self.be_offset.pack(side=tk.RIGHT)
        
    def create_trailing_stop_section(self):
        """Create trailing stop settings section."""
        section = self.create_section_frame("Trailing Stop Settings")
        
        # Enable/Disable
        self.ts_enabled = tk.BooleanVar(
            value=self.config_manager.config["trailing_stop"]["enabled"]
        )
        ttk.Checkbutton(
            section,
            text="Enable Trailing Stop",
            variable=self.ts_enabled
        ).pack(anchor="w", pady=5)
        
        # Start pips settings
        start_frame = ttk.Frame(section)
        start_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(start_frame, text="Start Distance (pips):").pack(side=tk.LEFT)
        self.ts_start = ttk.Entry(start_frame, width=10)
        self.ts_start.insert(
            0, 
            str(self.config_manager.config["trailing_stop"]["start_pips"])
        )
        self.ts_start.pack(side=tk.RIGHT)
        
        # Distance pips settings
        distance_frame = ttk.Frame(section)
        distance_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(distance_frame, text="Trail Distance (pips):").pack(side=tk.LEFT)
        self.ts_distance = ttk.Entry(distance_frame, width=10)
        self.ts_distance.insert(
            0, 
            str(self.config_manager.config["trailing_stop"]["distance_pips"])
        )
        self.ts_distance.pack(side=tk.RIGHT)
        
    def create_risk_management_section(self):
        """Create risk management settings section."""
        section = self.create_section_frame("Risk Management")
        
        # Daily target settings
        target_frame = ttk.Frame(section)
        target_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(target_frame, text="Daily Target (%):").pack(side=tk.LEFT)
        self.daily_target = ttk.Entry(target_frame, width=10)
        self.daily_target.insert(
            0, 
            str(self.config_manager.config["risk_management"]["daily_target"])
        )
        self.daily_target.pack(side=tk.RIGHT)
        
        # Stop on target
        self.stop_on_target = tk.BooleanVar(
            value=self.config_manager.config["risk_management"]["stop_on_target"]
        )
        ttk.Checkbutton(
            section,
            text="Stop Trading on Target",
            variable=self.stop_on_target
        ).pack(anchor="w", pady=5)
        
    def create_section_frame(self, title: str) -> ttk.LabelFrame:
        """Create a section frame with title."""
        frame = ttk.LabelFrame(
            self.container,
            text=title,
            padding=10
        )
        frame.pack(fill=tk.X, pady=10)
        return frame
        
    def create_action_buttons(self):
        """Create action buttons."""
        button_frame = ttk.Frame(self.container)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Save button
        save_button = ttk.Button(
            button_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            style="Accent.TButton"
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Reset button
        reset_button = ttk.Button(
            button_frame,
            text="↺ Reset to Default",
            command=self.reset_settings
        )
        reset_button.pack(side=tk.RIGHT, padx=5)
        
    def save_settings(self):
        """Save current settings."""
        try:
            # Validate inputs
            be_pips = float(self.be_pips.get())
            be_offset = float(self.be_offset.get())
            ts_start = float(self.ts_start.get())
            ts_distance = float(self.ts_distance.get())
            daily_target = float(self.daily_target.get())
            
            # Create new config
            new_config = {
                "break_even": {
                    "enabled": self.be_enabled.get(),
                    "pips": be_pips,
                    "offset": be_offset
                },
                "trailing_stop": {
                    "enabled": self.ts_enabled.get(),
                    "start_pips": ts_start,
                    "distance_pips": ts_distance
                },
                "risk_management": {
                    "daily_target": daily_target,
                    "stop_on_target": self.stop_on_target.get()
                }
            }
            
            # Save configuration
            if self.config_manager.save_config(new_config):
                messagebox.showinfo(
                    "Success",
                    "✅ Settings saved successfully!"
                )
                self.window.destroy()
            else:
                raise Exception("Failed to save configuration")
                
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter valid numbers for all fields"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to save settings: {str(e)}"
            )
            
    def reset_settings(self):
        """Reset settings to default values."""
        if messagebox.askyesno(
            "Confirm Reset",
            "Are you sure you want to reset all settings to default values?"
        ):
            self.config_manager.config = self.config_manager.DEFAULT_CONFIG
            self.window.destroy()
            AdvancedSettingsWindow(self.parent)

# Style configuration
def configure_styles():
    """Configure custom ttk styles."""
    style = ttk.Style()
    
    # Configure modern looking buttons
    style.configure(
        "Accent.TButton",
        background="#BB86FC",
        foreground="white",
        padding=10
    )
    
    # Configure section frames
    style.configure(
        "TLabelframe",
        background="#1E1E1E",
        padding=15
    )
    
    style.configure(
        "TLabelframe.Label",
        font=("Helvetica", 10, "bold")
    )

# Initialize styles
configure_styles()
