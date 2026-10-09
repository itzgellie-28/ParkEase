import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

class StaffManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Staff - MallPark")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f5f6fa')
        
        # Sample data
        self.session = {
            'username': 'Admin User',
            'user_type': 'admin',
            'user_id': 1
        }
        
        self.staff_members = [
            {'id': 1, 'username': 'Admin User', 'created_at': '2024-01-10 09:00', 'is_current': True},
            {'id': 2, 'username': 'john_doe', 'created_at': '2024-01-12 14:30', 'is_current': False},
            {'id': 3, 'username': 'jane_smith', 'created_at': '2024-01-15 11:15', 'is_current': False},
            {'id': 4, 'username': 'mike_johnson', 'created_at': '2024-01-18 16:45', 'is_current': False}
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg='#f5f6fa')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar and main content
        self.create_sidebar()
        self.create_main_content()
        
    def create_sidebar(self):
        # Sidebar
        self.sidebar = tk.Frame(
            self.main_container,
            bg='#2c3e50',
            width=250
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(self.sidebar, bg='#2c3e50', pady=20)
        logo_frame.pack(fill=tk.X, padx=20)
        logo_frame.pack_propagate(False)
        
        tk.Label(
            logo_frame,
            text="MallPark",
            bg='#2c3e50',
            fg='white',
            font=('Segoe UI', 20, 'bold')
        ).pack()
        
        tk.Label(
            logo_frame,
            text="Management System",
            bg='#2c3e50',
            fg='#3498db',
            font=('Segoe UI', 10)
        ).pack(pady=(5, 0))
        
        # Separator
        separator = tk.Frame(self.sidebar, bg='rgba(255,255,255,0.1)', height=1)
        separator.pack(fill=tk.X, padx=20, pady=20)
        
        # Navigation links
        nav_frame = tk.Frame(self.sidebar, bg='#2c3e50')
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        nav_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("🅿️ Park Vehicle", self.park_vehicle),
            ("📍 Parking Slots", self.show_slots),
            ("📊 History", self.show_history),
            ("👥 Manage Staff", self.manage_staff, True),  # Active
            ("📈 Reports", self.show_reports)
        ]
        
        self.nav_buttons = []
        for text, command, *active in nav_items:
            is_active = bool(active)
            btn_bg = '#3498db' if is_active else '#2c3e50'
            btn = tk.Button(
                nav_frame,
                text=text,
                bg=btn_bg,
                fg='white',
                font=('Segoe UI', 11),
                relief='flat',
                anchor='w',
                command=command
            )
            btn.pack(fill=tk.X, pady=5)
            self.nav_buttons.append(btn)
        
        # Sidebar footer
        footer_frame = tk.Frame(self.sidebar, bg='#2c3e50', pady=20)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20)
        
        # User info
        user_info_frame = tk.Frame(footer_frame, bg='#2c3e50')
        user_info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            user_info_frame,
            text=self.session['username'],
            bg='#2c3e50',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            anchor='w'
        ).pack(fill=tk.X)
        
        tk.Label(
            user_info_frame,
            text=self.session['user_type'].capitalize(),
            bg='#2c3e50',
            fg='#3498db',
            font=('Segoe UI', 10),
            anchor='w'
        ).pack(fill=tk.X)
        
        # Logout button
        logout_btn = tk.Button(
            footer_frame,
            text="🚪 Logout",
            bg='#e74c3c',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            command=self.logout
        )
        logout_btn.pack(fill=tk.X)
        
    def create_main_content(self):
        # Main content area
        self.main_content = tk.Frame(self.main_container, bg='#f5f6fa')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Staff table
        self.create_staff_table()
        
        # Flash messages area
        self.flash_frame = tk.Frame(self.main_content, bg='#f5f6fa')
        self.flash_frame.pack(fill=tk.X, pady=(10, 0))
        
    def create_header(self):
        # Header
        header_frame = tk.Frame(self.main_content, bg='white', relief='raised', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title and button container
        title_frame = tk.Frame(header_frame, bg='white', padx=20, pady=20)
        title_frame.pack(fill=tk.X)
        
        # Title
        title_label = tk.Label(
            title_frame,
            text="👥 Manage Staff",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        # Add Staff button
        add_staff_btn = tk.Button(
            title_frame,
            text="➕ Add New Staff",
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            command=self.add_staff,
            padx=15,
            pady=8
        )
        add_staff_btn.pack(side=tk.RIGHT)
        
        # Bind hover effects
        add_staff_btn.bind("<Enter>", lambda e: add_staff_btn.config(bg='#2980b9'))
        add_staff_btn.bind("<Leave>", lambda e: add_staff_btn.config(bg='#3498db'))
        
    def create_staff_table(self):
        # Staff table container
        table_container = tk.Frame(self.main_content, bg='white', relief='raised', bd=1)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        if not self.staff_members:
            self.show_empty_state(table_container)
        else:
            self.create_staff_table_content(table_container)
            
    def create_staff_table_content(self, parent):
        # Create treeview with scrollbar
        tree_frame = tk.Frame(parent, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create treeview
        columns = ('ID', 'Username', 'Created At', 'Actions')
        self.staff_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Define column headings
        column_widths = {'ID': 80, 'Username': 200, 'Created At': 150, 'Actions': 200}
        for col in columns:
            self.staff_tree.heading(col, text=col)
            self.staff_tree.column(col, width=column_widths.get(col, 120), anchor='center')
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        background="white",
                        foreground="black",
                        rowheight=35,
                        fieldbackground="white",
                        font=('Segoe UI', 10))
        
        style.configure("Treeview.Heading",
                        background="#f8f9fa",
                        foreground="#2c3e50",
                        font=('Segoe UI', 10, 'bold'),
                        relief='flat')
        
        style.map("Treeview", 
                 background=[('selected', '#f8f9fa')])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.staff_tree.yview)
        self.staff_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.staff_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate data
        self.populate_staff_data()
        
    def populate_staff_data(self):
        # Clear existing data
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
            
        # Add staff data to treeview
        for i, staff in enumerate(self.staff_members):
            # Determine actions text
            if staff.get('is_current', False):
                actions_text = "Current User"
            else:
                actions_text = "🗑️ Delete"
            
            values = (
                staff['id'],
                staff['username'],
                staff['created_at'],
                actions_text
            )
            
            # Insert into treeview
            item_id = self.staff_tree.insert('', 'end', values=values)
            
            # Store staff data in treeview item
            self.staff_tree.set(item_id, 'staff_data', staff)
            
            # Configure row colors
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            self.staff_tree.item(item_id, tags=tags)
        
        # Configure tag colors
        self.staff_tree.tag_configure('evenrow', background='#ffffff')
        self.staff_tree.tag_configure('oddrow', background='#f8f9fa')
        
        # Bind double-click for actions
        self.staff_tree.bind('<Double-1>', self.on_staff_action)
        
    def on_staff_action(self, event):
        selection = self.staff_tree.selection()
        if selection:
            item = selection[0]
            staff_data = self.staff_tree.set(item, 'staff_data')
            
            if staff_data and not staff_data.get('is_current', False):
                self.delete_staff_member(staff_data)
                
    def delete_staff_member(self, staff):
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete staff member '{staff['username']}'?\nThis action cannot be undone!"
        ):
            # Remove from data
            self.staff_members = [s for s in self.staff_members if s['id'] != staff['id']]
            
            # Show success message
            self.show_flash_message(f"Staff member '{staff['username']}' deleted successfully!", "success")
            
            # Refresh table
            self.refresh_staff_table()
            
    def refresh_staff_table(self):
        # Clear and repopulate table
        for item in self.staff_tree.get_children():
            self.staff_tree.delete(item)
        self.populate_staff_data()
        
    def show_empty_state(self, parent):
        empty_frame = tk.Frame(parent, bg='white')
        empty_frame.pack(expand=True)
        
        tk.Label(
            empty_frame,
            text="👥",
            bg='white',
            font=('Segoe UI', 48),
            pady=20
        ).pack()
        
        tk.Label(
            empty_frame,
            text="No Staff Members",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 16, 'bold')
        ).pack()
        
        tk.Label(
            empty_frame,
            text="There are no staff members in the system yet.",
            bg='white',
            fg='#7f8c8d',
            font=('Segoe UI', 12)
        ).pack(pady=10)
        
        add_btn = tk.Button(
            empty_frame,
            text="➕ Add First Staff Member",
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            command=self.add_staff,
            padx=15,
            pady=10
        )
        add_btn.pack(pady=20)
        
        # Bind hover effects
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg='#2980b9'))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg='#3498db'))
        
    def show_flash_message(self, message, category):
        """Show a flash message"""
        # Clear existing flash messages
        for widget in self.flash_frame.winfo_children():
            widget.destroy()
            
        # Determine colors based on category
        colors = {
            'success': ('#27ae60', 'white'),
            'error': ('#e74c3c', 'white')
        }
        bg_color, fg_color = colors.get(category, ('#3498db', 'white'))
        
        # Create message label
        message_label = tk.Label(
            self.flash_frame,
            text=message,
            bg=bg_color,
            fg=fg_color,
            font=('Segoe UI', 10, 'bold'),
            padx=15,
            pady=10,
            relief='raised',
            bd=1
        )
        message_label.pack(fill=tk.X)
        
        # Auto-hide after 5 seconds
        self.root.after(5000, lambda: message_label.pack_forget())
        
    def add_staff(self):
        # Create add staff window
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Staff Member")
        add_window.geometry("400x300")
        add_window.configure(bg='white')
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Center the window
        add_window.update_idletasks()
        x = (add_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (add_window.winfo_screenheight() // 2) - (300 // 2)
        add_window.geometry(f'400x300+{x}+{y}')
        
        # Header
        header_frame = tk.Frame(add_window, bg='#3498db', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="➕ Add Staff Member",
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 16, 'bold')
        ).pack(expand=True)
        
        # Form content
        form_frame = tk.Frame(add_window, bg='white', padx=30, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        tk.Label(
            form_frame,
            text="Username:",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        
        username_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1
        )
        username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        tk.Label(
            form_frame,
            text="Password:",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))
        
        password_entry = tk.Entry(
            form_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            show="•"
        )
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill=tk.X)
        
        def create_staff():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            # Create new staff member
            new_staff = {
                'id': max([s['id'] for s in self.staff_members]) + 1,
                'username': username,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'is_current': False
            }
            
            self.staff_members.append(new_staff)
            self.show_flash_message(f"Staff member '{username}' added successfully!", "success")
            self.refresh_staff_table()
            add_window.destroy()
        
        create_btn = tk.Button(
            button_frame,
            text="Create Staff",
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            command=create_staff,
            padx=15,
            pady=8
        )
        create_btn.pack(side=tk.LEFT)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            bg='#95a5a6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            command=add_window.destroy,
            padx=15,
            pady=8
        )
        cancel_btn.pack(side=tk.RIGHT)
        
    # Navigation methods
    def show_dashboard(self):
        messagebox.showinfo("Navigation", "Redirecting to Dashboard...")
        
    def park_vehicle(self):
        messagebox.showinfo("Navigation", "Redirecting to Park Vehicle...")
        
    def show_slots(self):
        messagebox.showinfo("Navigation", "Redirecting to Parking Slots...")
        
    def show_history(self):
        messagebox.showinfo("Navigation", "Redirecting to History...")
        
    def manage_staff(self):
        messagebox.showinfo("Navigation", "Already on Manage Staff")
        
    def show_reports(self):
        messagebox.showinfo("Navigation", "Redirecting to Reports...")
        
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = StaffManagementApp(root)
    root.mainloop()