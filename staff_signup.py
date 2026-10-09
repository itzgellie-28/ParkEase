import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class StaffSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff Sign Up - Mall Parking")
        self.root.geometry("500x800")
        self.root.configure(bg='#0a2463')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create animated background
        self.create_animated_background()
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 500
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_animated_background(self):
        """Create floating circles animation in the background"""
        self.canvas = tk.Canvas(self.root, bg='#0a2463', highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.circles = []
        circle_data = [
            (0.25, 80, 0),    # left: 25%, size: 80px, delay: 0s
            (0.10, 20, 2),    # left: 10%, size: 20px, delay: 2s
            (0.70, 20, 4),    # left: 70%, size: 20px, delay: 4s
            (0.40, 60, 0),    # left: 40%, size: 60px, delay: 0s
            (0.65, 20, 0)     # left: 65%, size: 20px, delay: 0s
        ]
        
        for left_ratio, size, delay in circle_data:
            circle = {
                'id': None,
                'x': left_ratio * 500,
                'y': 800 + size,  # Start below the window
                'size': size,
                'speed': random.uniform(1, 3),
                'rotation': 0
            }
            self.circles.append(circle)
        
        self.animate_circles()
        
    def animate_circles(self):
        """Animate the floating circles"""
        for circle in self.circles:
            if circle['id']:
                self.canvas.delete(circle['id'])
            
            # Move circle upward
            circle['y'] -= circle['speed']
            circle['rotation'] += 2
            
            # Reset if circle goes above the top
            if circle['y'] < -circle['size']:
                circle['y'] = 800 + circle['size']
                circle['x'] = random.uniform(0.1, 0.9) * 500
            
            # Create circle with semi-transparent effect
            circle['id'] = self.canvas.create_oval(
                circle['x'] - circle['size']/2,
                circle['y'] - circle['size']/2,
                circle['x'] + circle['size']/2,
                circle['y'] + circle['size']/2,
                fill='rgba(255,255,255,0.15)',
                outline=''
            )
        
        # Continue animation
        self.root.after(50, self.animate_circles)
        
    def setup_ui(self):
        # Main container
        self.container = tk.Frame(self.root, bg='#0a2463')
        self.container.place(relx=0.5, rely=0.5, anchor='center', width=450, height=700)
        
        # Card frame with glass morphism effect
        self.card = tk.Frame(
            self.container,
            bg='rgba(255,255,255,0.1)',
            relief='flat',
            bd=0,
            padx=30,
            pady=40
        )
        self.card.pack(fill=tk.BOTH, expand=True)
        
        # Create logo section
        self.create_logo_section()
        
        # Create form sections
        self.create_form_sections()
        
    def create_logo_section(self):
        # Logo frame
        logo_frame = tk.Frame(self.card, bg='rgba(255,255,255,0)')
        logo_frame.pack(pady=(0, 25))
        
        # Logo icon
        logo_icon_frame = tk.Frame(
            logo_frame,
            bg='white',
            width=40,
            height=40,
            relief='flat'
        )
        logo_icon_frame.pack(side=tk.LEFT, padx=(0, 10))
        logo_icon_frame.pack_propagate(False)
        
        logo_icon_label = tk.Label(
            logo_icon_frame,
            text="P",
            bg='white',
            fg='#3a5fc9',
            font=('Segoe UI', 18, 'bold')
        )
        logo_icon_label.pack(expand=True)
        
        # Logo text
        logo_text_label = tk.Label(
            logo_frame,
            text="MallPark",
            bg='rgba(255,255,255,0)',
            fg='white',
            font=('Segoe UI', 24, 'bold')
        )
        logo_text_label.pack(side=tk.LEFT)
        
        # Title
        title_label = tk.Label(
            self.card,
            text="Staff Registration",
            bg='rgba(255,255,255,0)',
            fg='white',
            font=('Segoe UI', 18, 'bold'),
            pady=(0, 25)
        )
        title_label.pack()
        
        # Staff badge
        staff_badge_frame = tk.Frame(
            self.card,
            bg='rgba(77,171,247,0.2)',
            relief='solid',
            bd=1,
            padx=15,
            pady=8
        )
        staff_badge_frame.pack(pady=(0, 20))
        
        badge_icon = tk.Label(
            staff_badge_frame,
            text="👤",
            bg='rgba(77,171,247,0.2)',
            fg='#4dabf7',
            font=('Segoe UI', 12)
        )
        badge_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        badge_text = tk.Label(
            staff_badge_frame,
            text="Parking Staff Account",
            bg='rgba(77,171,247,0.2)',
            fg='#4dabf7',
            font=('Segoe UI', 12)
        )
        badge_text.pack(side=tk.LEFT)
        
    def create_form_sections(self):
        # Flash messages area
        self.flash_frame = tk.Frame(self.card, bg='rgba(255,255,255,0)')
        self.flash_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Info box
        self.create_info_box()
        
        # Form
        self.create_registration_form()
        
        # Login links
        self.create_login_links()
        
    def create_info_box(self):
        info_frame = tk.Frame(
            self.card,
            bg='rgba(255,255,255,0.1)',
            relief='solid',
            bd=1,
            padx=15,
            pady=15
        )
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        info_title = tk.Label(
            info_frame,
            text="Staff Permissions:",
            bg='rgba(255,255,255,0)',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        info_title.pack(anchor='w')
        
        # Permissions list
        permissions = [
            "• Park and remove vehicles",
            "• View current parking slots", 
            "• Access recent history (7 days)",
            "• Generate QR codes"
        ]
        
        for permission in permissions:
            perm_label = tk.Label(
                info_frame,
                text=permission,
                bg='rgba(255,255,255,0)',
                fg='rgba(255,255,255,0.9)',
                font=('Segoe UI', 10),
                anchor='w'
            )
            perm_label.pack(anchor='w', pady=(2, 0))
            
    def create_registration_form(self):
        form_frame = tk.Frame(self.card, bg='rgba(255,255,255,0)')
        form_frame.pack(fill=tk.X)
        
        # Username field
        username_frame = tk.Frame(form_frame, bg='rgba(255,255,255,0)')
        username_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Segoe UI', 12),
            bg='rgba(255,255,255,0.15)',
            fg='white',
            insertbackground='white',
            relief='solid',
            bd=1,
            width=30
        )
        self.username_entry.pack(fill=tk.X, ipady=8)
        self.username_entry.insert(0, "Staff Username")
        self.username_entry.bind('<FocusIn>', self.clear_placeholder)
        self.username_entry.bind('<FocusOut>', self.restore_placeholder)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg='rgba(255,255,255,0)')
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 12),
            bg='rgba(255,255,255,0.15)',
            fg='white',
            insertbackground='white',
            relief='solid',
            bd=1,
            show="•",
            width=30
        )
        self.password_entry.pack(fill=tk.X, ipady=8)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', self.clear_placeholder_password)
        self.password_entry.bind('<FocusOut>', self.restore_placeholder_password)
        
        # Confirm Password field
        confirm_frame = tk.Frame(form_frame, bg='rgba(255,255,255,0)')
        confirm_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.confirm_entry = tk.Entry(
            confirm_frame,
            font=('Segoe UI', 12),
            bg='rgba(255,255,255,0.15)',
            fg='white',
            insertbackground='white',
            relief='solid',
            bd=1,
            show="•",
            width=30
        )
        self.confirm_entry.pack(fill=tk.X, ipady=8)
        self.confirm_entry.insert(0, "Confirm Password")
        self.confirm_entry.bind('<FocusIn>', self.clear_placeholder_confirm)
        self.confirm_entry.bind('<FocusOut>', self.restore_placeholder_confirm)
        
        # Register button
        register_btn = tk.Button(
            form_frame,
            text="Register Staff Account",
            bg='#4dabf7',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            command=self.register_staff,
            pady=12
        )
        register_btn.pack(fill=tk.X, pady=(10, 15))
        
        # Bind hover effects
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg='#339af0'))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg='#4dabf7'))
        
    def create_login_links(self):
        links_frame = tk.Frame(self.card, bg='rgba(255,255,255,0)')
        links_frame.pack(fill=tk.X)
        
        # Back to Login link
        login_link = tk.Label(
            links_frame,
            text="Back to Login",
            bg='rgba(255,255,255,0)',
            fg='#a5d8ff',
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2'
        )
        login_link.pack()
        login_link.bind("<Button-1>", lambda e: self.back_to_login())
        
        # Separator
        separator = tk.Label(
            links_frame,
            text=" | ",
            bg='rgba(255,255,255,0)',
            fg='rgba(255,255,255,0.8)',
            font=('Segoe UI', 10)
        )
        separator.pack()
        
        # Admin Setup link
        admin_link = tk.Label(
            links_frame,
            text="Admin Setup",
            bg='rgba(255,255,255,0)',
            fg='#a5d8ff',
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2'
        )
        admin_link.pack()
        admin_link.bind("<Button-1>", lambda e: self.admin_setup())
        
    def clear_placeholder(self, event):
        if self.username_entry.get() == "Staff Username":
            self.username_entry.delete(0, tk.END)
            self.username_entry.configure(fg='white')
            
    def restore_placeholder(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Staff Username")
            self.username_entry.configure(fg='rgba(255,255,255,0.6)')
            
    def clear_placeholder_password(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, tk.END)
            self.password_entry.configure(fg='white', show="•")
            
    def restore_placeholder_password(self, event):
        if not self.password_entry.get():
            self.password_entry.configure(show="")
            self.password_entry.insert(0, "Password")
            self.password_entry.configure(fg='rgba(255,255,255,0.6)')
            
    def clear_placeholder_confirm(self, event):
        if self.confirm_entry.get() == "Confirm Password":
            self.confirm_entry.delete(0, tk.END)
            self.confirm_entry.configure(fg='white', show="•")
            
    def restore_placeholder_confirm(self, event):
        if not self.confirm_entry.get():
            self.confirm_entry.configure(show="")
            self.confirm_entry.insert(0, "Confirm Password")
            self.confirm_entry.configure(fg='rgba(255,255,255,0.6)')
            
    def show_flash_message(self, message, category="info"):
        """Show a flash message"""
        # Clear existing flash messages
        for widget in self.flash_frame.winfo_children():
            widget.destroy()
            
        # Create message label
        message_label = tk.Label(
            self.flash_frame,
            text=message,
            bg='rgba(255,255,255,0.9)',
            fg='#333',
            font=('Segoe UI', 10, 'bold'),
            padx=12,
            pady=12,
            relief='raised',
            bd=1
        )
        message_label.pack(fill=tk.X)
        
        # Auto-hide after 5 seconds
        self.root.after(5000, lambda: message_label.pack_forget())
        
    def register_staff(self):
        """Handle staff registration"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        
        # Validation
        if username in ["", "Staff Username"]:
            messagebox.showerror("Error", "Please enter a username")
            self.username_entry.focus()
            return
            
        if password in ["", "Password"]:
            messagebox.showerror("Error", "Please enter a password")
            self.password_entry.focus()
            return
            
        if confirm_password in ["", "Confirm Password"]:
            messagebox.showerror("Error", "Please confirm your password")
            self.confirm_entry.focus()
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            self.confirm_entry.focus()
            return
            
        # Show success message
        self.show_flash_message(f"Staff account '{username}' created successfully!")
        messagebox.showinfo("Success", f"Staff account '{username}' has been registered!")
        
        # Reset form
        self.reset_form()
        
    def reset_form(self):
        """Reset the form to initial state"""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "Staff Username")
        self.username_entry.configure(fg='rgba(255,255,255,0.6)')
        
        self.password_entry.delete(0, tk.END)
        self.password_entry.configure(show="")
        self.password_entry.insert(0, "Password")
        self.password_entry.configure(fg='rgba(255,255,255,0.6)')
        
        self.confirm_entry.delete(0, tk.END)
        self.confirm_entry.configure(show="")
        self.confirm_entry.insert(0, "Confirm Password")
        self.confirm_entry.configure(fg='rgba(255,255,255,0.6)')
        
    def back_to_login(self):
        """Handle back to login action"""
        if messagebox.askyesno("Confirm", "Return to Login page?"):
            self.root.quit()
            
    def admin_setup(self):
        """Handle admin setup navigation"""
        messagebox.showinfo("Admin Setup", "Redirecting to Admin Setup page...")

if __name__ == "__main__":
    root = tk.Tk()
    app = StaffSignupApp(root)
    root.mainloop()