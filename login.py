import tkinter as tk
from tkinter import messagebox, ttk
import logging
import mt5_mock as mt5
from utils import login_manager
from painel import PainelApp
import ctypes

class LoginApp:
    """Login window for FutureMT5 application."""
    
    def __init__(self, root):
        """Initialize the login window with modern UI elements."""
        self.root = root
        self.setup_window()
        self.create_ui_elements()
        self.load_saved_credentials()
        
    def setup_window(self):
        """Configure the main window properties."""
        self.root.title("Future MT5 - Login")
        self.root.geometry("500x600")
        self.center_window(500, 600)
        self.root.resizable(False, False)
        self.apply_modern_style()
        
        # Theme configuration
        self.theme = "dark"
        self.colors = self.get_theme_colors()
        self.root.configure(bg=self.colors["bg"])
        
    def get_theme_colors(self):
        """Get color scheme based on current theme."""
        return {
            "bg": "#121212" if self.theme == "dark" else "#F0F0F0",
            "fg": "#FFFFFF" if self.theme == "dark" else "#000000",
            "card": "#1E1E1E" if self.theme == "dark" else "#FFFFFF",
            "input_bg": "#2E2E2E" if self.theme == "dark" else "#F8F8F8",
            "button": "#BB86FC",
            "button_hover": "#9965E5",
            "error": "#CF6679",
            "success": "#03DAC6"
        }

    def create_ui_elements(self):
        """Create and arrange UI elements with modern styling."""
        # Main container
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Logo and title
        self.create_header()
        
        # Login card
        self.create_login_card()
        
        # Theme toggle
        self.create_theme_toggle()
        
    def create_header(self):
        """Create header with logo and title."""
        header_frame = tk.Frame(self.container, bg=self.colors["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            header_frame,
            text="🚀 Future MT5",
            font=("Helvetica", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="Trading Automation Platform",
            font=("Helvetica", 12),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        subtitle.pack()

    def create_login_card(self):
        """Create the main login form card."""
        self.card = tk.Frame(
            self.container,
            bg=self.colors["card"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["button"],
            highlightcolor=self.colors["button"]
        )
        self.card.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Login form
        self.create_login_form()

    def create_login_form(self):
        """Create login form elements."""
        # Server
        tk.Label(
            self.card,
            text="MT5 Server",
            bg=self.colors["card"],
            fg=self.colors["fg"],
            font=("Helvetica", 10)
        ).pack(pady=(20, 5))
        
        self.entry_server = self.create_entry()
        
        # Login
        tk.Label(
            self.card,
            text="Login ID",
            bg=self.colors["card"],
            fg=self.colors["fg"],
            font=("Helvetica", 10)
        ).pack(pady=(15, 5))
        
        self.entry_login = self.create_entry()
        
        # Password
        tk.Label(
            self.card,
            text="Password",
            bg=self.colors["card"],
            fg=self.colors["fg"],
            font=("Helvetica", 10)
        ).pack(pady=(15, 5))
        
        self.entry_password = self.create_entry(show="•")
        
        # Checkboxes
        self.create_checkboxes()
        
        # Login button
        self.create_login_button()

    def create_entry(self, show=None):
        """Create a styled entry widget."""
        entry = tk.Entry(
            self.card,
            font=("Helvetica", 12),
            bg=self.colors["input_bg"],
            fg=self.colors["fg"],
            insertbackground=self.colors["fg"],
            relief="flat",
            show=show
        )
        entry.pack(fill=tk.X, padx=30)
        return entry

    def create_checkboxes(self):
        """Create checkbox options."""
        checkbox_frame = tk.Frame(self.card, bg=self.colors["card"])
        checkbox_frame.pack(fill=tk.X, padx=30, pady=15)
        
        # Real account checkbox
        self.check_real = tk.BooleanVar()
        real_cb = tk.Checkbutton(
            checkbox_frame,
            text="Real Account",
            variable=self.check_real,
            bg=self.colors["card"],
            fg=self.colors["fg"],
            selectcolor=self.colors["card"],
            activebackground=self.colors["card"]
        )
        real_cb.pack(side=tk.LEFT)
        
        # Save login checkbox
        self.check_save = tk.BooleanVar()
        save_cb = tk.Checkbutton(
            checkbox_frame,
            text="Remember Me",
            variable=self.check_save,
            bg=self.colors["card"],
            fg=self.colors["fg"],
            selectcolor=self.colors["card"],
            activebackground=self.colors["card"]
        )
        save_cb.pack(side=tk.RIGHT)

    def create_login_button(self):
        """Create the login button."""
        self.login_button = tk.Button(
            self.card,
            text="LOGIN",
            command=self.connect,
            bg=self.colors["button"],
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            activebackground=self.colors["button_hover"],
            cursor="hand2"
        )
        self.login_button.pack(fill=tk.X, padx=30, pady=20)

    def create_theme_toggle(self):
        """Create theme toggle button."""
        self.theme_button = tk.Button(
            self.root,
            text="🌙" if self.theme == "light" else "☀️",
            command=self.toggle_theme,
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            bd=0,
            font=("Helvetica", 12),
            cursor="hand2"
        )
        self.theme_button.place(x=450, y=10)

    def connect(self):
        """Handle MT5 connection attempt."""
        try:
            self.login_button.config(state="disabled", text="Connecting...")
            self.root.update()
            
            server = self.entry_server.get()
            login = int(self.entry_login.get())
            password = self.entry_password.get()
            
            # Validate inputs
            if not all([server, login, password]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            # Initialize MT5 connection
            if not mt5.initialize(server=server, login=login, password=password):
                error = mt5.last_error()
                messagebox.showerror("Connection Error", f"Failed to connect: {error}")
                logging.error(f"MT5 connection error: {error}")
                return
            
            # Save credentials if requested
            if self.check_save.get():
                login_manager.save_login(server, login, password)
            
            messagebox.showinfo("Success", "✅ Connected successfully!")
            
            # Launch main application
            self.root.destroy()
            root = tk.Tk()
            app = PainelApp(root, self.theme)
            root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            logging.error(f"Login error: {str(e)}")
        finally:
            self.login_button.config(state="normal", text="LOGIN")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "light" if self.theme == "dark" else "dark"
        self.colors = self.get_theme_colors()
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to all elements."""
        self.root.configure(bg=self.colors["bg"])
        self.container.configure(bg=self.colors["bg"])
        self.card.configure(
            bg=self.colors["card"],
            highlightbackground=self.colors["button"]
        )
        
        # Update all widgets with new theme
        for widget in self.card.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.colors["card"], fg=self.colors["fg"])
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=self.colors["input_bg"],
                    fg=self.colors["fg"],
                    insertbackground=self.colors["fg"]
                )
            elif isinstance(widget, tk.Checkbutton):
                widget.configure(
                    bg=self.colors["card"],
                    fg=self.colors["fg"],
                    selectcolor=self.colors["card"],
                    activebackground=self.colors["card"]
                )
        
        self.login_button.configure(
            bg=self.colors["button"],
            activebackground=self.colors["button_hover"]
        )
        
        self.theme_button.configure(
            text="🌙" if self.theme == "light" else "☀️",
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def apply_modern_style(self):
        """Apply modern window styling."""
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            class MARGINS(ctypes.Structure):
                _fields_ = [
                    ("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int)
                ]
            margins = MARGINS(2, 2, 2, 2)
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
        except:
            logging.warning("Failed to apply modern window style")

    def load_saved_credentials(self):
        """Load saved login credentials if available."""
        try:
            saved_data = login_manager.load_login()
            if saved_data:
                self.entry_server.insert(0, saved_data.get("server", ""))
                self.entry_login.insert(0, str(saved_data.get("login", "")))
                self.entry_password.insert(0, saved_data.get("password", ""))
                self.check_save.set(True)
        except Exception as e:
            logging.error(f"Error loading saved credentials: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
