import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import json

class ReportsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MallPark - Reports")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f5f6fa')
        
        # Colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'background': '#f5f6fa'
        }
        
        # Sample data (replace with your actual data source)
        self.vehicle_stats = [
            {'vehicle_type': 'Car', 'count': 45},
            {'vehicle_type': 'Motorcycle', 'count': 23},
            {'vehicle_type': 'Truck', 'count': 12}
        ]
        
        self.activity_data = [
            {'date': '2024-01-15', 'vehicles_processed': 8},
            {'date': '2024-01-14', 'vehicles_processed': 12},
            {'date': '2024-01-13', 'vehicles_processed': 6},
            {'date': '2024-01-12', 'vehicles_processed': 15},
            {'date': '2024-01-11', 'vehicles_processed': 9}
        ]
        
        self.staff_activity = [
            {'username': 'john_doe', 'vehicles_processed': 25},
            {'username': 'jane_smith', 'vehicles_processed': 18},
            {'username': 'bob_wilson', 'vehicles_processed': 12},
            {'username': 'alice_brown', 'vehicles_processed': 20}
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar and main content
        self.create_sidebar(main_container)
        self.create_main_content(main_container)
        
    def create_sidebar(self, parent):
        # Sidebar frame
        sidebar = tk.Frame(parent, bg=self.colors['primary'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        logo_frame.pack(fill=tk.X, padx=20, pady=20)
        
        logo_title = tk.Label(logo_frame, text="MallPark", font=('Arial', 16, 'bold'), 
                             fg='white', bg=self.colors['primary'])
        logo_title.pack()
        
        logo_subtitle = tk.Label(logo_frame, text="Management System", 
                                font=('Arial', 10), fg='white', bg=self.colors['primary'])
        logo_subtitle.pack()
        
        # Navigation
        nav_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        nav_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Navigation buttons
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Park Vehicle", self.park_vehicle),
            ("Parking Slots", self.show_slots),
            ("History", self.show_history),
            ("Manage Staff", self.manage_staff),
            ("Reports", self.show_reports)
        ]
        
        for text, command in nav_items:
            btn = tk.Button(nav_frame, text=text, font=('Arial', 10),
                           bg=self.colors['secondary'] if text == "Reports" else self.colors['primary'],
                           fg='white', bd=0, anchor='w', padx=15, pady=12,
                           command=command)
            btn.pack(fill=tk.X, pady=2)
        
        # User info and logout
        user_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        user_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=20)
        
        user_name = tk.Label(user_frame, text="Admin User", font=('Arial', 11, 'bold'),
                            fg='white', bg=self.colors['primary'])
        user_name.pack(anchor='w')
        
        user_role = tk.Label(user_frame, text="Administrator", font=('Arial', 9),
                            fg=self.colors['secondary'], bg=self.colors['primary'])
        user_role.pack(anchor='w')
        
        logout_btn = tk.Button(user_frame, text="Logout", font=('Arial', 10, 'bold'),
                              bg=self.colors['danger'], fg='white', bd=0,
                              padx=15, pady=10, command=self.logout)
        logout_btn.pack(fill=tk.X, pady=(10, 0))
        
    def create_main_content(self, parent):
        # Main content frame
        main_content = tk.Frame(parent, bg=self.colors['background'])
        main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_content, bg='white', relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_title = tk.Label(header_frame, text="System Reports", 
                               font=('Arial', 18, 'bold'), bg='white', fg=self.colors['dark'])
        header_title.pack(side=tk.LEFT, padx=20, pady=20)
        
        current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_label = tk.Label(header_frame, text=f"Last updated: {current_date}",
                             font=('Arial', 10), bg='white', fg='gray')
        date_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Statistics cards
        self.create_stats_cards(main_content)
        
        # Vehicle type statistics
        self.create_vehicle_stats(main_content)
        
        # Recent activity
        self.create_recent_activity(main_content)
        
        # Staff performance
        self.create_staff_performance(main_content)
        
    def create_stats_cards(self, parent):
        stats_frame = tk.Frame(parent, bg=self.colors['background'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Calculate totals
        total_vehicles = sum(vehicle['count'] for vehicle in self.vehicle_stats)
        total_activity_days = len(self.activity_data)
        total_staff = len(self.staff_activity)
        
        stats_data = [
            (total_vehicles, "Total Vehicles Processed", "#3498db"),
            (total_activity_days, "Days of Activity", "#27ae60"),
            (total_staff, "Active Staff Members", "#f39c12")
        ]
        
        for i, (count, label, color) in enumerate(stats_data):
            card = tk.Frame(stats_frame, bg='white', relief=tk.RAISED, bd=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20) if i < 2 else (0, 0))
            
            # Icon and count
            count_label = tk.Label(card, text=str(count), font=('Arial', 24, 'bold'),
                                  bg='white', fg=color)
            count_label.pack(pady=(20, 5))
            
            # Label
            label_text = tk.Label(card, text=label, font=('Arial', 10),
                                 bg='white', fg='gray')
            label_text.pack(pady=(0, 20))
            
    def create_vehicle_stats(self, parent):
        section_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Section header
        header_frame = tk.Frame(section_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title = tk.Label(header_frame, text="Vehicle Type Statistics", 
                        font=('Arial', 16, 'bold'), bg='white', fg=self.colors['dark'])
        title.pack(side=tk.LEFT)
        
        # Create treeview for table
        tree_frame = tk.Frame(section_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        tree = ttk.Treeview(tree_frame, columns=('Type', 'Count', 'Percentage'), 
                           show='headings', yscrollcommand=scrollbar.set)
        
        # Configure columns
        tree.heading('Type', text='Vehicle Type')
        tree.heading('Count', text='Count')
        tree.heading('Percentage', text='Percentage')
        
        tree.column('Type', width=200)
        tree.column('Count', width=100)
        tree.column('Percentage', width=100)
        
        # Add data
        total_vehicles = sum(vehicle['count'] for vehicle in self.vehicle_stats)
        
        for vehicle in self.vehicle_stats:
            percentage = (vehicle['count'] / total_vehicles * 100) if total_vehicles > 0 else 0
            tree.insert('', 'end', values=(
                vehicle['vehicle_type'],
                vehicle['count'],
                f"{percentage:.1f}%"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
        
    def create_recent_activity(self, parent):
        section_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Section header
        header_frame = tk.Frame(section_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title = tk.Label(header_frame, text="Recent Activity (Last 30 Days)", 
                        font=('Arial', 16, 'bold'), bg='white', fg=self.colors['dark'])
        title.pack(side=tk.LEFT)
        
        # Create treeview for table
        tree_frame = tk.Frame(section_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        tree = ttk.Treeview(tree_frame, columns=('Date', 'Vehicles Processed'), 
                           show='headings', yscrollcommand=scrollbar.set)
        
        # Configure columns
        tree.heading('Date', text='Date')
        tree.heading('Vehicles Processed', text='Vehicles Processed')
        
        tree.column('Date', width=200)
        tree.column('Vehicles Processed', width=150)
        
        # Add data
        for activity in self.activity_data:
            tree.insert('', 'end', values=(
                activity['date'],
                activity['vehicles_processed']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
        
    def create_staff_performance(self, parent):
        section_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        section_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Section header
        header_frame = tk.Frame(section_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title = tk.Label(header_frame, text="Staff Performance", 
                        font=('Arial', 16, 'bold'), bg='white', fg=self.colors['dark'])
        title.pack(side=tk.LEFT)
        
        # Create treeview for table
        tree_frame = tk.Frame(section_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        tree = ttk.Treeview(tree_frame, columns=('Staff Member', 'Vehicles Processed'), 
                           show='headings', yscrollcommand=scrollbar.set)
        
        # Configure columns
        tree.heading('Staff Member', text='Staff Member')
        tree.heading('Vehicles Processed', text='Vehicles Processed')
        
        tree.column('Staff Member', width=200)
        tree.column('Vehicles Processed', width=150)
        
        # Add data
        for staff in self.staff_activity:
            tree.insert('', 'end', values=(
                staff['username'],
                staff['vehicles_processed']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)
    
    # Navigation methods
    def show_dashboard(self):
        messagebox.showinfo("Navigation", "Redirecting to Dashboard")
        
    def park_vehicle(self):
        messagebox.showinfo("Navigation", "Redirecting to Park Vehicle")
        
    def show_slots(self):
        messagebox.showinfo("Navigation", "Redirecting to Parking Slots")
        
    def show_history(self):
        messagebox.showinfo("Navigation", "Redirecting to History")
        
    def manage_staff(self):
        messagebox.showinfo("Navigation", "Redirecting to Manage Staff")
        
    def show_reports(self):
        messagebox.showinfo("Navigation", "Already on Reports page")
        
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = ReportsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()