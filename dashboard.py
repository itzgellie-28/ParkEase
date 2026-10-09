import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
from datetime import datetime
import random

class ParkingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ParkEase - Dashboard System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#667eea')
        
        # Sample data
        self.session = {
            'username': 'John Doe',
            'user_type': 'staff'  # Change to 'admin' to see admin features
        }
        
        self.vehicles = [
            {'plate_number': 'ABC123', 'vehicle_type': 'Car', 'slot_number': 'A12', 
             'time_in': '10:30 AM', 'staff_in': 'John Doe', 'has_qr': True},
            {'plate_number': 'XYZ789', 'vehicle_type': 'Motorcycle', 'slot_number': 'B05', 
             'time_in': '11:15 AM', 'staff_in': 'Jane Smith', 'has_qr': True},
            {'plate_number': 'DEF456', 'vehicle_type': 'Truck', 'slot_number': 'C08', 
             'time_in': '09:45 AM', 'staff_in': 'System', 'has_qr': False}
        ]
        
        self.stats = {
            'available_slots': 37,
            'occupied_slots': 13,
            'total_slots': 50,
            'active_vehicles': len(self.vehicles)
        }
        
        self.setup_ui()
        self.update_datetime()
        
    def setup_ui(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg='#667eea')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Dashboard container (sidebar + main content)
        self.dashboard_frame = tk.Frame(self.main_container, bg='white')
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_sidebar()
        self.create_main_content()
        
    def create_sidebar(self):
        # Sidebar
        self.sidebar = tk.Frame(
            self.dashboard_frame,
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
            text="ParkEase",
            bg='#2c3e50',
            fg='white',
            font=('Segoe UI', 20, 'bold')
        ).pack()
        
        tk.Label(
            logo_frame,
            text="Dashboard System",
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
            ("🏠 Dashboard", self.show_dashboard, True),
            ("🅿️ Park Vehicle", self.park_vehicle, False),
            ("📍 Parking Slots", self.show_slots, False),
            ("📊 History", self.show_history, False)
        ]
        
        if self.session['user_type'] == 'admin':
            nav_items.extend([
                ("👥 Manage Staff", self.manage_staff, False),
                ("📈 Reports", self.show_reports, False)
            ])
        
        self.nav_buttons = []
        for text, command, is_active in nav_items:
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
        self.main_content = tk.Frame(self.dashboard_frame, bg='#f8f9fa')
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_header()
        self.create_stats_grid()
        self.create_active_vehicles_section()
        self.create_quick_actions()
        
    def create_header(self):
        # Header
        header_frame = tk.Frame(self.main_content, bg='white', relief='raised', bd=1)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Welcome section
        welcome_frame = tk.Frame(header_frame, bg='white')
        welcome_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Label(
            welcome_frame,
            text=f"Welcome back, {self.session['username']}! 👋",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 18, 'bold')
        ).pack(anchor='w')
        
        tk.Label(
            welcome_frame,
            text="Manage your parking facility efficiently",
            bg='white',
            fg='#95a5a6',
            font=('Segoe UI', 12)
        ).pack(anchor='w', pady=(5, 0))
        
        # Date display
        self.date_frame = tk.Frame(header_frame, bg='#3498db')
        self.date_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.date_label = tk.Label(
            self.date_frame,
            text="",
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            padx=15,
            pady=10
        )
        self.date_label.pack()
        
    def create_stats_grid(self):
        # Stats grid
        stats_frame = tk.Frame(self.main_content, bg='#f8f9fa')
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Stats cards
        stats_data = [
            ("🚗", "Available Slots", self.stats['available_slots'], "#27ae60"),
            ("🅿️", "Occupied Slots", self.stats['occupied_slots'], "#f39c12"),
            ("📊", "Total Slots", self.stats['total_slots'], "#3498db"),
            ("💰", "Active Vehicles", self.stats['active_vehicles'], "#e74c3c")
        ]
        
        self.stats_cards = []
        for icon, label, value, color in stats_data:
            card = tk.Frame(
                stats_frame,
                bg='white',
                relief='raised',
                bd=1,
                width=200,
                height=120
            )
            card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 15))
            card.pack_propagate(False)
            
            # Icon
            tk.Label(
                card,
                text=icon,
                bg='white',
                font=('Segoe UI', 24),
                pady=10
            ).pack()
            
            # Value
            value_label = tk.Label(
                card,
                text=str(value),
                bg='white',
                fg='#2c3e50',
                font=('Segoe UI', 24, 'bold')
            )
            value_label.pack()
            
            # Label
            tk.Label(
                card,
                text=label,
                bg='white',
                fg='#95a5a6',
                font=('Segoe UI', 11)
            ).pack(pady=(5, 15))
            
            self.stats_cards.append(card)
            
            # Bind hover events
            card.bind("<Enter>", lambda e, c=card: self.on_card_enter(c))
            card.bind("<Leave>", lambda e, c=card: self.on_card_leave(c))
            
    def create_active_vehicles_section(self):
        # Active vehicles section
        section_frame = tk.Frame(self.main_content, bg='white', relief='raised', bd=1)
        section_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Section header
        header_frame = tk.Frame(section_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=25, pady=20)
        
        tk.Label(
            header_frame,
            text="📋 Active Vehicles",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 16, 'bold')
        ).pack(side=tk.LEFT)
        
        # Action buttons
        actions_frame = tk.Frame(header_frame, bg='white')
        actions_frame.pack(side=tk.RIGHT)
        
        park_btn = tk.Button(
            actions_frame,
            text="🅿️ Park New Vehicle",
            bg='#3498db',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            command=self.park_vehicle
        )
        park_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        slots_btn = tk.Button(
            actions_frame,
            text="📍 View All Slots",
            bg='#27ae60',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief='flat',
            command=self.show_slots
        )
        slots_btn.pack(side=tk.LEFT)
        
        # Vehicles table
        self.create_vehicles_table(section_frame)
        
    def create_vehicles_table(self, parent):
        # Table container
        table_container = tk.Frame(parent, bg='white')
        table_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))
        
        if not self.vehicles:
            # Empty state
            empty_frame = tk.Frame(table_container, bg='white')
            empty_frame.pack(expand=True)
            
            tk.Label(
                empty_frame,
                text="🚗",
                bg='white',
                font=('Segoe UI', 48),
                pady=20
            ).pack()
            
            tk.Label(
                empty_frame,
                text="No Active Vehicles",
                bg='white',
                fg='#2c3e50',
                font=('Segoe UI', 16, 'bold')
            ).pack()
            
            tk.Label(
                empty_frame,
                text="There are currently no vehicles parked in the facility.",
                bg='white',
                fg='#95a5a6',
                font=('Segoe UI', 12)
            ).pack(pady=10)
            
            tk.Button(
                empty_frame,
                text="🅿️ Park First Vehicle",
                bg='#3498db',
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                relief='flat',
                command=self.park_vehicle
            ).pack(pady=20)
            
        else:
            # Create table using Treeview
            columns = ('Plate', 'Type', 'Slot', 'Time In', 'QR Code', 'Parked By', 'Action')
            self.vehicles_table = ttk.Treeview(
                parent,
                columns=columns,
                show='headings',
                height=len(self.vehicles)
            )
            
            # Define headings
            for col in columns:
                self.vehicles_table.heading(col, text=col)
                self.vehicles_table.column(col, width=120)
            
            # Add data
            for vehicle in self.vehicles:
                vehicle_type = vehicle['vehicle_type']
                type_color = {
                    'Car': '#1976d2',
                    'Motorcycle': '#7b1fa2', 
                    'Truck': '#388e3c'
                }.get(vehicle_type, '#95a5a6')
                
                qr_text = "📱 View QR" if vehicle['has_qr'] else "No QR"
                parked_by = vehicle['staff_in'] if vehicle['staff_in'] != 'System' else 'System'
                
                self.vehicles_table.insert('', 'end', values=(
                    vehicle['plate_number'],
                    vehicle_type,
                    vehicle['slot_number'],
                    vehicle['time_in'],
                    qr_text,
                    parked_by,
                    "❌ Remove"
                ))
            
            # Style the treeview
            style = ttk.Style()
            style.configure("Treeview", 
                          background="white",
                          foreground="black",
                          rowheight=35,
                          fieldbackground="white")
            style.configure("Treeview.Heading",
                          background="#f8f9fa",
                          foreground="#2c3e50",
                          font=('Segoe UI', 10, 'bold'))
            
            self.vehicles_table.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))
            
            # Bind remove action
            self.vehicles_table.bind('<Double-1>', self.on_remove_vehicle)
            
    def create_quick_actions(self):
        # Quick actions section
        section_frame = tk.Frame(self.main_content, bg='white', relief='raised', bd=1)
        section_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Section header
        header_frame = tk.Frame(section_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=25, pady=20)
        
        tk.Label(
            header_frame,
            text="⚡ Quick Actions",
            bg='white',
            fg='#2c3e50',
            font=('Segoe UI', 16, 'bold')
        ).pack(anchor='w')
        
        # Action buttons grid
        actions_grid = tk.Frame(section_frame, bg='white')
        actions_grid.pack(fill=tk.X, padx=25, pady=(0, 20))
        
        actions = [
            ("🅿️ Park Vehicle", self.park_vehicle, '#3498db'),
            ("📍 View Slots", self.show_slots, '#27ae60'),
            ("📊 View History", self.show_history, '#6c757d')
        ]
        
        if self.session['user_type'] == 'admin':
            actions.append(("👥 Manage Staff", self.manage_staff, '#17a2b8'))
        
        for text, command, color in actions:
            btn = tk.Button(
                actions_grid,
                text=text,
                bg=color,
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                relief='flat',
                command=command,
                width=15,
                height=2
            )
            btn.pack(side=tk.LEFT, padx=(0, 15))
            
    def on_card_enter(self, card):
        card.configure(relief='sunken')
        
    def on_card_leave(self, card):
        card.configure(relief='raised')
        
    def on_remove_vehicle(self, event):
        item = self.vehicles_table.selection()[0]
        values = self.vehicles_table.item(item, 'values')
        plate_number = values[0]
        
        if messagebox.askyesno("Confirm Removal", 
                             f"Are you sure you want to remove vehicle {plate_number}?"):
            # Remove from data
            self.vehicles = [v for v in self.vehicles if v['plate_number'] != plate_number]
            self.vehicles_table.delete(item)
            self.stats['active_vehicles'] = len(self.vehicles)
            self.stats['occupied_slots'] = max(0, self.stats['occupied_slots'] - 1)
            self.stats['available_slots'] = min(self.stats['total_slots'], 
                                              self.stats['available_slots'] + 1)
            
            messagebox.showinfo("Success", f"Vehicle {plate_number} removed successfully!")
            
    def update_datetime(self):
        current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p")
        self.date_label.config(text=current_time)
        self.root.after(1000, self.update_datetime)
        
    def show_dashboard(self):
        messagebox.showinfo("Navigation", "Already on Dashboard")
        
    def park_vehicle(self):
        messagebox.showinfo("Navigation", "Opening Park Vehicle form...")
        
    def show_slots(self):
        messagebox.showinfo("Navigation", "Opening Parking Slots...")
        
    def show_history(self):
        messagebox.showinfo("Navigation", "Opening History...")
        
    def manage_staff(self):
        if self.session['user_type'] == 'admin':
            messagebox.showinfo("Navigation", "Opening Staff Management...")
        else:
            messagebox.showerror("Access Denied", "Admin access required")
            
    def show_reports(self):
        if self.session['user_type'] == 'admin':
            messagebox.showinfo("Navigation", "Opening Reports...")
        else:
            messagebox.showerror("Access Denied", "Admin access required")
            
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingDashboard(root)
    root.mainloop()