import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional
from utils import ThemeManager, WindowManager, MT5Helper
from estrategia import FutureBreakout
from configuracoes_avancadas import AdvancedSettingsWindow

class PainelApp:
    """Main trading panel application."""
    
    def __init__(self, root: tk.Tk, theme: str = "dark"):
        """Initialize the main trading panel."""
        self.root = root
        self.theme = theme
        self.strategy: Optional[FutureBreakout] = None
        
        self.setup_window()
        self.create_ui()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("Future MT5 - Trading Panel")
        self.root.geometry("800x600")
        WindowManager.center_window(self.root, 800, 600)
        self.root.resizable(True, True)
        WindowManager.apply_modern_style(self.root)
        
        # Apply theme
        ThemeManager.apply_theme(self.root, self.theme)
        
    def create_ui(self):
        """Create the user interface."""
        # Main container
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create sections
        self.create_header()
        self.create_trading_section()
        self.create_log_section()
        
    def create_header(self):
        """Create header section with controls."""
        header = ttk.Frame(self.container)
        header.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title = ttk.Label(
            header,
            text="🚀 Trading Dashboard",
            font=("Helvetica", 20, "bold")
        )
        title.pack(side=tk.LEFT)
        
        # Controls frame
        controls = ttk.Frame(header)
        controls.pack(side=tk.RIGHT)
        
        # Settings button
        settings_btn = ttk.Button(
            controls,
            text="⚙️ Settings",
            command=self.open_settings,
            style="Accent.TButton"
        )
        settings_btn.pack(side=tk.RIGHT, padx=5)
        
        # Theme toggle
        theme_btn = ttk.Button(
            controls,
            text="🌙" if self.theme == "light" else "☀️",
            command=self.toggle_theme
        )
        theme_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_trading_section(self):
        """Create trading controls section."""
        trading = ttk.LabelFrame(
            self.container,
            text="Trading Controls",
            padding=10
        )
        trading.pack(fill=tk.X, pady=(0, 20))
        
        # Symbol selection
        symbol_frame = ttk.Frame(trading)
        symbol_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(symbol_frame, text="Symbol:").pack(side=tk.LEFT)
        
        self.symbol_var = tk.StringVar()
        symbol_cb = ttk.Combobox(
            symbol_frame,
            textvariable=self.symbol_var,
            values=[s[0] for s in MT5Helper.get_symbols()],
            state="readonly",
            width=20
        )
        symbol_cb.pack(side=tk.LEFT, padx=(5, 20))
        
        # Timeframe selection
        ttk.Label(symbol_frame, text="Timeframe:").pack(side=tk.LEFT)
        
        self.timeframe_var = tk.StringVar()
        timeframe_cb = ttk.Combobox(
            symbol_frame,
            textvariable=self.timeframe_var,
            values=list(MT5Helper.get_timeframes().keys()),
            state="readonly",
            width=20
        )
        timeframe_cb.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = ttk.Frame(trading)
        volume_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT)
        
        self.volume_var = tk.StringVar(value="0.1")
        volume_entry = ttk.Entry(
            volume_frame,
            textvariable=self.volume_var,
            width=10
        )
        volume_entry.pack(side=tk.LEFT, padx=5)
        
        # Start/Stop buttons
        button_frame = ttk.Frame(trading)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.start_btn = ttk.Button(
            button_frame,
            text="▶️ Start Trading",
            command=self.start_trading,
            style="Accent.TButton"
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="⏹️ Stop Trading",
            command=self.stop_trading,
            state="disabled"
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
    def create_log_section(self):
        """Create logging section."""
        log_frame = ttk.LabelFrame(
            self.container,
            text="Trading Log",
            padding=10
        )
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text widget
        self.log_text = tk.Text(
            log_frame,
            height=10,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.log_text.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
    def open_settings(self):
        """Open advanced settings window."""
        AdvancedSettingsWindow(self.root)
        
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "light" if self.theme == "dark" else "dark"
        ThemeManager.apply_theme(self.root, self.theme)
        
    def start_trading(self):
        """Start the trading strategy."""
        try:
            # Validate inputs
            symbol = self.symbol_var.get()
            timeframe_str = self.timeframe_var.get()
            
            if not symbol:
                messagebox.showerror("Error", "Please select a symbol")
                return
                
            if not timeframe_str:
                messagebox.showerror("Error", "Please select a timeframe")
                return
                
            try:
                volume = float(self.volume_var.get())
                if volume <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid volume")
                return
                
            # Get timeframe value
            timeframes = MT5Helper.get_timeframes()
            timeframe = timeframes[timeframe_str]
            
            # Create and start strategy
            self.strategy = FutureBreakout(
                symbol=symbol,
                volume=volume,
                timeframe=timeframe,
                logger=self.log_text
            )
            
            # Update UI
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            
            # Start strategy in separate thread
            import threading
            self.strategy_thread = threading.Thread(
                target=self.strategy.execute,
                daemon=True
            )
            self.strategy_thread.start()
            
            self.log_text.insert(
                'end',
                "✅ Trading strategy started\n"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start trading: {str(e)}")
            logging.error(f"Start trading error: {str(e)}")
            
    def stop_trading(self):
        """Stop the trading strategy."""
        try:
            if self.strategy:
                # Strategy will stop on next iteration
                self.strategy = None
                
                # Update UI
                self.start_btn.configure(state="normal")
                self.stop_btn.configure(state="disabled")
                
                self.log_text.insert(
                    'end',
                    "🛑 Trading strategy stopped\n"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop trading: {str(e)}")
            logging.error(f"Stop trading error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PainelApp(root)
    root.mainloop()
