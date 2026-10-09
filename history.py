import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

class ParkingHistoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking History")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f4f8')
        
        # Sample history data
        self.history_data = [
            {
                'slot_number': 'A12', 'plate_number': 'ABC123', 'vehicle_type': 'Car',
                'time_in': '2024-01-15 10:30 AM', 'time_out': '2024-01-15 02:45 PM',
                'fee': '₱150.00', 'staff_in': 'John Doe', 'staff_out': 'Jane Smith',
                'has_qr': True, 'status': 'completed'
            },
            {
                'slot_number': 'B05', 'plate_number': 'XYZ789', 'vehicle_type': 'Motorcycle',
                'time_in': '2024-01-15 09:15 AM', 'time_out': '2024-01-15 01:30 PM',
                'fee': '₱75.00', 'staff_in': 'Mike Johnson', 'staff_out': 'System',
                'has_qr': True, 'status': 'completed'
            },
            {
                'slot_number': 'C08', 'plate_number': 'DEF456', 'vehicle_type': 'Truck',
                'time_in': '2024-01-14 11:00 AM', 'time_out': '2024-01-14 06:20 PM',
                'fee': '₱300.00', 'staff_in': 'System', 'staff_out': 'John Doe',
                'has_qr': False, 'status': 'completed'
            },
            {
                'slot_number': 'A15', 'plate_number': 'GHI789', 'vehicle_type': 'Car',
                'time_in': '2024-01-14 03:45 PM', 'time_out': 'Active',
                'fee': '₱0.00', 'staff_in': 'Jane Smith', 'staff_out': 'N/A',
                'has_qr': True, 'status': 'active'
            }
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        self.create_header()
        
        # Main content
        self.create_main_content()
        
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(
            self.root,
            bg='#3D6A9F',
            height=120
        )
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(header_frame, bg='#3D6A9F')
        title_frame.pack(expand=True)
        
        tk.Label(
            title_frame,
            text="📊 Parking History",
            bg='#3D6A9F',
            fg='white',
            font=('Arial', 24, 'bold'),
            pady=10
        ).pack()
        
        # Navigation
        nav_frame = tk.Frame(header_frame, bg='#3D6A9F')
        nav_frame.pack(pady=(0, 15))
        
        back_btn = tk.Button(
            nav_frame,
            text="🏠 Back to Dashboard",
            bg='#5284BD',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='flat',
            command=self.back_to_dashboard,
            padx=15,
            pady=6
        )
        back_btn.pack()
        
        # Bind hover effects
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg='#3D6A9F'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg='#5284BD'))
        
    def create_main_content(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f4f8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        if not self.history_data:
            self.show_empty_state(main_frame)
        else:
            self.create_history_table(main_frame)
            
    def create_history_table(self, parent):
        # Table container with scrollbar
        table_container = tk.Frame(parent, bg='#f0f4f8')
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for the table and scrollbar
        table_frame = tk.Frame(table_container, bg='#f0f4f8')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(
            table_frame,
            columns=('Slot', 'Plate', 'Type', 'Time In', 'Time Out', 'Fee', 'Parked By', 'Removed By', 'QR Code', 'Details', 'Actions'),
            show='headings',
            height=15
        )
        
        # Define column headings
        columns = {
            'Slot': 80, 'Plate': 100, 'Type': 100, 'Time In': 120, 'Time Out': 120,
            'Fee': 80, 'Parked By': 100, 'Removed By': 100, 'QR Code': 80,
            'Details': 80, 'Actions': 150
        }
        
        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        background="white",
                        foreground="black",
                        rowheight=35,
                        fieldbackground="white",
                        font=('Arial', 10))
        
        style.configure("Treeview.Heading",
                        background="#5284BD",
                        foreground="white",
                        font=('Arial', 10, 'bold'),
                        relief='flat')
        
        style.map("Treeview", 
                 background=[('selected', '#B0C4E3')])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate data
        self.populate_table_data()
        
        # Bind double-click event for details
        self.tree.bind('<Double-1>', self.on_view_details)
        
    def populate_table_data(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add data to treeview
        for i, vehicle in enumerate(self.history_data):
            # Determine row color
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            
            # Add vehicle type styling
            vehicle_type = vehicle['vehicle_type'].lower()
            
            # Create values for display
            values = (
                vehicle['slot_number'],
                vehicle['plate_number'],
                vehicle['vehicle_type'],
                vehicle['time_in'],
                vehicle['time_out'],
                vehicle['fee'],
                vehicle['staff_in'],
                vehicle['staff_out'],
                "📱 QR Code" if vehicle['has_qr'] else "No QR",
                "👁️ View",
                "🔄 Restore | 🗑️ Delete"
            )
            
            self.tree.insert('', 'end', values=values, tags=tags, iid=str(i))
        
        # Configure tag colors
        self.tree.tag_configure('evenrow', background='#E3EDF7')
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        
    def on_view_details(self, event):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            vehicle_index = int(item)
            vehicle = self.history_data[vehicle_index]
            
            self.show_vehicle_details(vehicle)
            
    def show_vehicle_details(self, vehicle):
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Vehicle Details - {vehicle['plate_number']}")
        details_window.geometry("500x400")
        details_window.configure(bg='white')
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Header
        header_frame = tk.Frame(details_window, bg='#5284BD', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"🚗 {vehicle['plate_number']}",
            bg='#5284BD',
            fg='white',
            font=('Arial', 18, 'bold')
        ).pack(expand=True)
        
        # Details content
        content_frame = tk.Frame(details_window, bg='white', padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        details = [
            ("Slot Number", vehicle['slot_number']),
            ("Vehicle Type", vehicle['vehicle_type']),
            ("Time In", vehicle['time_in']),
            ("Time Out", vehicle['time_out']),
            ("Parking Fee", vehicle['fee']),
            ("Parked By", vehicle['staff_in']),
            ("Removed By", vehicle['staff_out']),
            ("QR Code", "Available" if vehicle['has_qr'] else "Not Available"),
            ("Status", "Active" if vehicle['status'] == 'active' else "Completed")
        ]
        
        for label, value in details:
            row_frame = tk.Frame(content_frame, bg='white')
            row_frame.pack(fill=tk.X, pady=8)
            
            tk.Label(
                row_frame,
                text=f"{label}:",
                bg='white',
                fg='#2c3e50',
                font=('Arial', 11, 'bold'),
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row_frame,
                text=value,
                bg='white',
                fg='#7f8c8d',
                font=('Arial', 11),
                anchor='w'
            ).pack(side=tk.LEFT)
        
        # Action buttons
        button_frame = tk.Frame(content_frame, bg='white', pady=20)
        button_frame.pack(fill=tk.X)
        
        if vehicle['status'] == 'completed':
            restore_btn = tk.Button(
                button_frame,
                text="🔄 Restore Vehicle",
                bg='#4CAF50',
                fg='white',
                font=('Arial', 11, 'bold'),
                relief='flat',
                command=lambda: self.restore_vehicle(vehicle, details_window),
                padx=15,
                pady=8
            )
            restore_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Delete Record",
            bg='#F44336',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='flat',
            command=lambda: self.delete_vehicle(vehicle, details_window),
            padx=15,
            pady=8
        )
        delete_btn.pack(side=tk.LEFT)
        
        close_btn = tk.Button(
            button_frame,
            text="✖️ Close",
            bg='#6c757d',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='flat',
            command=details_window.destroy,
            padx=15,
            pady=8
        )
        close_btn.pack(side=tk.RIGHT)
        
    def restore_vehicle(self, vehicle, window):
        if messagebox.askyesno(
            "Confirm Restore",
            f"Restore vehicle {vehicle['plate_number']} to active parking list?"
        ):
            messagebox.showinfo(
                "Success",
                f"Vehicle {vehicle['plate_number']} has been restored to active parking!"
            )
            window.destroy()
            # Here you would update your data and refresh the table
            
    def delete_vehicle(self, vehicle, window):
        if messagebox.askyesno(
            "Confirm Delete",
            f"Permanently delete record for {vehicle['plate_number']}?\nThis action cannot be undone!"
        ):
            # Remove from data
            self.history_data = [v for v in self.history_data if v['plate_number'] != vehicle['plate_number']]
            
            messagebox.showinfo(
                "Success",
                f"Record for {vehicle['plate_number']} has been deleted!"
            )
            window.destroy()
            self.refresh_table()
            
    def refresh_table(self):
        # Clear and repopulate table
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_table_data()
        
    def show_empty_state(self, parent):
        empty_frame = tk.Frame(parent, bg='#f0f4f8')
        empty_frame.pack(expand=True)
        
        tk.Label(
            empty_frame,
            text="📊",
            bg='#f0f4f8',
            font=('Arial', 48),
            pady=20
        ).pack()
        
        tk.Label(
            empty_frame,
            text="No History Records",
            bg='#f0f4f8',
            fg='#2c3e50',
            font=('Arial', 18, 'bold')
        ).pack()
        
        tk.Label(
            empty_frame,
            text="No parking history available yet.",
            bg='#f0f4f8',
            fg='#7f8c8d',
            font=('Arial', 12)
        ).pack(pady=10)
        
    def back_to_dashboard(self):
        if messagebox.askyesno("Confirm", "Return to Dashboard?"):
            self.root.quit()

    def create_context_menu(self):
        # Right-click context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="View Details", command=self.on_view_details)
        self.context_menu.add_command(label="Restore Vehicle", command=self.on_restore_vehicle)
        self.context_menu.add_command(label="Delete Record", command=self.on_delete_vehicle)
        
        # Bind right-click
        self.tree.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
            
    def on_restore_vehicle(self):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            vehicle_index = int(item)
            vehicle = self.history_data[vehicle_index]
            self.restore_vehicle(vehicle, self.root)
            
    def on_delete_vehicle(self):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            vehicle_index = int(item)
            vehicle = self.history_data[vehicle_index]
            self.delete_vehicle(vehicle, self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingHistoryApp(root)
    
    # Create context menu after app initialization
    app.create_context_menu()
    
    root.mainloop()