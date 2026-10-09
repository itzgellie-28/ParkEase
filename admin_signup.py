import tkinter as tk
from tkinter import ttk, messagebox
import re

class AdminSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Setup - Mall Parking")
        self.root.geometry("600x700")
        self.root.configure(bg='#0a2463')
        self.root.resizable(False, False)
        
        # Set up the main frame
        self.main_frame = tk.Frame(root, bg='#0a2463')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Card frame (main container)
        self.card = tk.Frame(
            self.main_frame, 
            bg='#1e3c8b',
            relief=tk.RAISED,
            bd=1,
            padx=30,
            pady=40
        )
        self.card.pack(fill=tk.BOTH, expand=True)
        
        # Logo section
        self.logo_frame = tk.Frame(self.card, bg='#1e3c8b')
        self.logo_frame.pack(pady=(0, 25))
        
        self.logo_icon = tk.Label(
            self.logo_frame,
            text="P",
            bg='white',
            fg='#3a5fc9',
            font=('Segoe UI', 18, 'bold'),
            width=3,
            height=1,
            relief=tk.FLAT
        )
        self.logo_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.logo_text = tk.Label(
            self.logo_frame,
            text="MallPark",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 24, 'bold')
        )
        self.logo_text.pack(side=tk.LEFT)
        
        # Title
        self.title_label = tk.Label(
            self.card,
            text="Admin Account Setup",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 18, 'bold')
        )
        self.title_label.pack(pady=(0, 25))
        
        # Admin badge
        self.admin_badge = tk.Label(
            self.card,
            text=" System Administrator",
            bg='#ffc107',
            fg='#856404',
            font=('Segoe UI', 12),
            relief=tk.RAISED,
            bd=1,
            padx=15,
            pady=8
        )
        self.admin_badge.pack(pady=(0, 20))
        
        # Info box
        self.info_frame = tk.Frame(
            self.card,
            bg='#3a5fc9',
            relief=tk.RAISED,
            bd=1,
            padx=15,
            pady=15
        )
        self.info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_title = tk.Label(
            self.info_frame,
            text="Important:",
            bg='#3a5fc9',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            justify=tk.LEFT
        )
        info_title.pack(anchor=tk.W)
        
        info_text = "• Admin accounts have full system access\n• Can manage staff accounts\n• Can view all reports and statistics\n• Can modify system settings"
        info_content = tk.Label(
            self.info_frame,
            text=info_text,
            bg='#3a5fc9',
            fg='white',
            font=('Segoe UI', 10),
            justify=tk.LEFT
        )
        info_content.pack(anchor=tk.W, pady=(5, 0))
        
        # Form frame
        self.form_frame = tk.Frame(self.card, bg='#1e3c8b')
        self.form_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Username field
        self.username_label = tk.Label(
            self.form_frame,
            text="Admin Username:",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 10),
            anchor=tk.W
        )
        self.username_label.pack(fill=tk.X, pady=(0, 5))
        
        self.username_entry = tk.Entry(
            self.form_frame,
            font=('Segoe UI', 12),
            bg='#3a5fc9',
            fg='white',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        self.password_label = tk.Label(
            self.form_frame,
            text="Password:",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 10),
            anchor=tk.W
        )
        self.password_label.pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = tk.Entry(
            self.form_frame,
            font=('Segoe UI', 12),
            bg='#3a5fc9',
            fg='white',
            show="•",
            insertbackground='white',
            relief=tk.FLAT
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm Password field
        self.confirm_password_label = tk.Label(
            self.form_frame,
            text="Confirm Password:",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 10),
            anchor=tk.W
        )
        self.confirm_password_label.pack(fill=tk.X, pady=(0, 5))
        
        self.confirm_password_entry = tk.Entry(
            self.form_frame,
            font=('Segoe UI', 12),
            bg='#3a5fc9',
            fg='white',
            show="•",
            insertbackground='white',
            relief=tk.FLAT
        )
        self.confirm_password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Secret Key field
        self.secret_key_label = tk.Label(
            self.form_frame,
            text="Admin Secret Key:",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 10),
            anchor=tk.W
        )
        self.secret_key_label.pack(fill=tk.X, pady=(0, 5))
        
        self.secret_key_entry = tk.Entry(
            self.form_frame,
            font=('Segoe UI', 12),
            bg='#3a5fc9',
            fg='white',
            insertbackground='white',
            relief=tk.FLAT
        )
        self.secret_key_entry.pack(fill=tk.X, pady=(0, 5))
        
        secret_key_hint = tk.Label(
            self.form_frame,
            text="Default secret key: admin123",
            bg='#1e3c8b',
            fg='#a5d8ff',
            font=('Segoe UI', 10),
            anchor=tk.W
        )
        secret_key_hint.pack(fill=tk.X, pady=(0, 15))
        
        # Submit button
        self.submit_button = tk.Button(
            self.form_frame,
            text="Create Admin Account",
            bg='#ff6b6b',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            command=self.submit_form
        )
        self.submit_button.pack(fill=tk.X, pady=(10, 15))
        
        # Links frame
        self.links_frame = tk.Frame(self.card, bg='#1e3c8b')
        self.links_frame.pack(fill=tk.X)
        
        self.back_link = tk.Label(
            self.links_frame,
            text="Back to Login",
            bg='#1e3c8b',
            fg='#a5d8ff',
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2'
        )
        self.back_link.pack(side=tk.LEFT)
        self.back_link.bind("<Button-1>", lambda e: self.back_to_login())
        
        self.separator = tk.Label(
            self.links_frame,
            text=" | ",
            bg='#1e3c8b',
            fg='white',
            font=('Segoe UI', 10)
        )
        self.separator.pack(side=tk.LEFT, padx=5)
        
        self.staff_link = tk.Label(
            self.links_frame,
            text="Staff Signup",
            bg='#1e3c8b',
            fg='#a5d8ff',
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2'
        )
        self.staff_link.pack(side=tk.LEFT)
        self.staff_link.bind("<Button-1>", lambda e: self.staff_signup())
        
        # Center the links
        self.links_frame.pack_configure(anchor=tk.CENTER)
        
    def submit_form(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        secret_key = self.secret_key_entry.get()
        
        # Validation
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
            
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            self.confirm_password_entry.focus_set()
            return
            
        if not secret_key:
            messagebox.showerror("Error", "Please enter the admin secret key")
            return
            
        if secret_key != "admin123":
            messagebox.showerror("Error", "Invalid admin secret key")
            return
            
        # If all validations pass
        messagebox.showinfo("Success", "Admin account created successfully!")
        # Here you would typically save the admin credentials
        
    def back_to_login(self):
        messagebox.showinfo("Info", "Redirecting to login page")
        # Add navigation logic here
        
    def staff_signup(self):
        messagebox.showinfo("Info", "Redirecting to staff signup page")
        # Add navigation logic here

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminSetupApp(root)
    root.mainloop()