import tkinter as tk
from tkinter import ttk, messagebox
import time

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - MallPark")
        self.root.geometry("500x700")
        self.root.configure(bg='#3a5fc9')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # User type (staff/admin)
        self.user_type = "staff"
        
        # Flash messages storage
        self.flash_messages = []
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 500
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Main login container
        self.login_container = tk.Frame(
            self.root,
            bg='white',
            padx=40,
            pady=40
        )
        self.login_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Logo section
        self.create_logo_section()
        
        # Flash messages section
        self.create_flash_messages_section()
        
        # Login form
        self.create_login_form()
        
        # Admin info
        self.create_admin_info()
        
        # Signup links
        self.create_signup_links()
        
    def create_logo_section(self):
        logo_frame = tk.Frame(self.login_container, bg='white')
        logo_frame.pack(pady=(0, 30))
        
        tk.Label(
            logo_frame,
            text="MallPark",
            bg='white',
            fg='#3a5fc9',
            font=('Segoe UI', 28, 'bold')
        ).pack()
        
        tk.Label(
            logo_frame,
            text="Parking Management System",
            bg='white',
            fg='#666',
            font=('Segoe UI', 12)
        ).pack(pady=(5, 0))
        
    def create_flash_messages_section(self):
        self.flash_frame = tk.Frame(self.login_container, bg='white')
        self.flash_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add sample flash messages (you can remove these in production)
        self.add_flash_message("Welcome to MallPark!", "info")
        
    def add_flash_message(self, message, category):
        """Add a flash message to the display"""
        message_frame = tk.Frame(self.flash_frame, bg='white')
        message_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Determine colors based on category
        colors = {
            'success': ('#d4edda', '#155724'),
            'error': ('#f8d7da', '#721c24'),
            'info': ('#d1ecf1', '#0c5460')
        }
        bg_color, fg_color = colors.get(category, ('#d1ecf1', '#0c5460'))
        
        message_label = tk.Label(
            message_frame,
            text=message,
            bg=bg_color,
            fg=fg_color,
            font=('Segoe UI', 10),
            padx=10,
            pady=10,
            wraplength=320,
            justify=tk.LEFT
        )
        message_label.pack(fill=tk.X)
        
        # Auto-hide after 5 seconds
        self.root.after(5000, lambda: self.hide_flash_message(message_label))
        
    def hide_flash_message(self, message_label):
        """Hide a flash message with fade effect"""
        try:
            message_label.pack_forget()
        except:
            pass
        
    def create_login_form(self):
        form_frame = tk.Frame(self.login_container, bg='white')
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Login options (Staff/Admin)
        self.create_login_options(form_frame)
        
        # Form fields
        self.create_form_fields(form_frame)
        
        # Login button
        self.create_login_button(form_frame)
        
    def create_login_options(self, parent):
        options_frame = tk.Frame(parent, bg='white')
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Staff option
        self.staff_option = tk.Frame(
            options_frame,
            bg='#f0f5ff',
            relief='solid',
            bd=2,
            padx=10,
            pady=10,
            width=150,
            height=60
        )
        self.staff_option.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 5))
        self.staff_option.pack_propagate(False)
        self.staff_option.bind("<Button-1>", lambda e: self.select_login_type("staff"))
        
        # Admin option
        self.admin_option = tk.Frame(
            options_frame,
            bg='white',
            relief='solid',
            bd=2,
            padx=10,
            pady=10,
            width=150,
            height=60
        )
        self.admin_option.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(5, 0))
        self.admin_option.pack_propagate(False)
        self.admin_option.bind("<Button-1>", lambda e: self.select_login_type("admin"))
        
        # Staff option content
        staff_icon = tk.Label(
            self.staff_option,
            text="👤",
            bg='#f0f5ff',
            font=('Segoe UI', 16)
        )
        staff_icon.pack()
        
        staff_text = tk.Label(
            self.staff_option,
            text="Staff",
            bg='#f0f5ff',
            font=('Segoe UI', 11, 'bold')
        )
        staff_text.pack()
        
        # Admin option content
        admin_icon = tk.Label(
            self.admin_option,
            text="🛡️",
            bg='white',
            font=('Segoe UI', 16)
        )
        admin_icon.pack()
        
        admin_text = tk.Label(
            self.admin_option,
            text="Admin",
            bg='white',
            font=('Segoe UI', 11, 'bold')
        )
        admin_text.pack()
        
        # Set initial border colors
        self.staff_option.configure(highlightbackground='#3a5fc9', highlightcolor='#3a5fc9')
        self.admin_option.configure(highlightbackground='#ddd', highlightcolor='#ddd')
        
    def select_login_type(self, login_type):
        self.user_type = login_type
        
        if login_type == "staff":
            self.staff_option.configure(bg='#f0f5ff', highlightbackground='#3a5fc9')
            self.admin_option.configure(bg='white', highlightbackground='#ddd')
            
            # Update staff labels
            for widget in self.staff_option.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg='#f0f5ff')
            
            # Update admin labels  
            for widget in self.admin_option.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg='white')
                    
        else:  # admin
            self.staff_option.configure(bg='white', highlightbackground='#ddd')
            self.admin_option.configure(bg='#f0f5ff', highlightbackground='#3a5fc9')
            
            # Update staff labels
            for widget in self.staff_option.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg='white')
            
            # Update admin labels
            for widget in self.admin_option.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg='#f0f5ff')
        
        # Show/hide admin info
        if login_type == "admin":
            self.admin_info.pack(fill=tk.X, pady=(15, 0))
        else:
            self.admin_info.pack_forget()
            
    def create_form_fields(self, parent):
        # Username field
        username_frame = tk.Frame(parent, bg='white')
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white'
        )
        self.username_entry.pack(fill=tk.X, ipady=8)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind('<FocusIn>', self.clear_placeholder)
        self.username_entry.bind('<FocusOut>', self.restore_placeholder)
        
        # Password field
        password_frame = tk.Frame(parent, bg='white')
        password_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white',
            show="•"
        )
        self.password_entry.pack(fill=tk.X, ipady=8)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', self.clear_placeholder_password)
        self.password_entry.bind('<FocusOut>', self.restore_placeholder_password)
        
    def clear_placeholder(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, tk.END)
            self.username_entry.configure(fg='black')
            
    def restore_placeholder(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Username")
            self.username_entry.configure(fg='gray')
            
    def clear_placeholder_password(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.configure(fg='black', show="•")
            
    def restore_placeholder_password(self, event):
        if not self.password_entry.get():
            self.password_entry.configure(show="")
            self.password_entry.insert(0, "Password")
            self.password_entry.configure(fg='gray')
            
    def create_login_button(self, parent):
        self.login_button = tk.Button(
            parent,
            text="Login",
            bg='#3a5fc9',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            cursor='hand2',
            command=self.perform_login,
            height=2
        )
        self.login_button.pack(fill=tk.X, pady=(10, 0))
        
        # Bind hover effects
        self.login_button.bind("<Enter>", lambda e: self.login_button.config(bg='#2a4fb9'))
        self.login_button.bind("<Leave>", lambda e: self.login_button.config(bg='#3a5fc9'))
        
    def create_admin_info(self):
        self.admin_info = tk.Frame(
            self.login_container,
            bg='#fff3cd',
            relief='solid',
            bd=1,
            padx=10,
            pady=10
        )
        # Initially hidden for staff login
        # self.admin_info.pack(fill=tk.X, pady=(15, 0))
        
        info_text = "Admin Login: For system administrators only"
        tk.Label(
            self.admin_info,
            text=info_text,
            bg='#fff3cd',
            fg='#856404',
            font=('Segoe UI', 10),
            justify=tk.LEFT,
            wraplength=320
        ).pack()
        
    def create_signup_links(self):
        links_frame = tk.Frame(self.login_container, bg='white')
        links_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Admin signup link
        admin_signup_link = tk.Label(
            links_frame,
            text="First Time Admin Setup",
            bg='white',
            fg='#3a5fc9',
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2'
        )
        admin_signup_link.pack()
        admin_signup_link.bind("<Button-1>", lambda e: self.show_admin_signup())
        
        # Info text
        info_text = tk.Label(
            links_frame,
            text="Staff registration requires admin access.",
            bg='white',
            fg='#666',
            font=('Segoe UI', 9),
            pady=(10, 0)
        )
        info_text.pack()
        
    def perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validation
        if username in ["", "Username"] or password in ["", "Password"]:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        # Show loading state
        self.show_loading_state()
        
        # Simulate login process
        self.root.after(2000, lambda: self.complete_login(username, password))
        
    def show_loading_state(self):
        self.login_button.config(
            text="Logging in...",
            state='disabled',
            bg='#2a4fb9'
        )
        
    def complete_login(self, username, password):
        # Reset button state
        self.login_button.config(
            text="Login",
            state='normal',
            bg='#3a5fc9'
        )
        
        # Simulate login validation
        if username == "admin" and password == "admin123" and self.user_type == "admin":
            messagebox.showinfo("Success", f"Welcome Admin {username}!")
            # Here you would navigate to admin dashboard
        elif username == "staff" and password == "staff123" and self.user_type == "staff":
            messagebox.showinfo("Success", f"Welcome Staff {username}!")
            # Here you would navigate to staff dashboard
        else:
            messagebox.showerror("Error", "Invalid credentials or user type mismatch")
            
    def show_admin_signup(self):
        messagebox.showinfo("Admin Setup", "Redirecting to Admin Setup page...")
        # Here you would navigate to admin setup page

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()