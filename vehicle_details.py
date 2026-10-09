import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

class VehicleDetailsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Details - MallPark")
        self.root.geometry("600x700")
        self.root.configure(bg='#E3EDF7')
        
        # Center the window
        self.center_window()
        
        # Sample vehicle data
        self.vehicle = {
            'slot_number': 'A12',
            'plate_number': 'ABC123',
            'vehicle_type': 'Car',
            'time_in': '2024-01-15 10:30:45',
            'time_out': '2024-01-15 14:45:20',
            'fee': '₱150.00',
            'has_qr': True,
            'status': 'completed'
        }
        
        # Alternative sample data for active vehicle
        # self.vehicle = {
        #     'slot_number': 'B05',
        #     'plate_number': 'XYZ789',
        #     'vehicle_type': 'Motorcycle',
        #     'time_in': '2024-01-15 13:15:30',
        #     'time_out': None,
        #     'fee': None,
        #     'has_qr': True,
        #     'status': 'active'
        # }
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 600
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#E3EDF7', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Details card
        self.create_details_card(main_frame)
        
    def create_details_card(self, parent):
        # Card frame
        card_frame = tk.Frame(
            parent,
            bg='#E3EDF7',
            relief='raised',
            bd=1,
            padx=25,
            pady=25
        )
        card_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            card_frame,
            text="Vehicle Details",
            bg='#E3EDF7',
            fg='#3D6A9F',
            font=('Arial', 20, 'bold'),
            pady=(0, 20)
        )
        title_label.pack()
        
        # Details content
        self.create_details_content(card_frame)
        
        # QR Code section
        self.create_qr_section(card_frame)
        
        # Back button
        self.create_back_button(card_frame)
        
    def create_details_content(self, parent):
        # Create a frame for details with better organization
        details_frame = tk.Frame(parent, bg='#E3EDF7')
        details_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Vehicle details data
        details_data = [
            ("Slot:", self.vehicle['slot_number']),
            ("Plate Number:", self.vehicle['plate_number']),
            ("Vehicle Type:", self.vehicle['vehicle_type']),
            ("Time In:", self.vehicle['time_in']),
            ("Time Out:", self.vehicle['time_out'] or 'Still Parked'),
            ("Fee:", self.vehicle['fee'] or 'Not yet calculated')
        ]
        
        for label_text, value_text in details_data:
            self.create_detail_row(details_frame, label_text, value_text)
            
    def create_detail_row(self, parent, label_text, value_text):
        """Create a single detail row with label and value"""
        row_frame = tk.Frame(parent, bg='#E3EDF7')
        row_frame.pack(fill=tk.X, pady=8)
        
        # Label
        label = tk.Label(
            row_frame,
            text=label_text,
            bg='#E3EDF7',
            fg='#2F4F7F',
            font=('Arial', 14, 'bold'),
            width=15,
            anchor='w'
        )
        label.pack(side=tk.LEFT)
        
        # Value
        value = tk.Label(
            row_frame,
            text=value_text,
            bg='#E3EDF7',
            fg='#2F4F7F',
            font=('Arial', 14),
            anchor='w'
        )
        value.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def create_qr_section(self, parent):
        """Create QR code section"""
        qr_frame = tk.Frame(parent, bg='#E3EDF7')
        qr_frame.pack(fill=tk.X, pady=(10, 20))
        
        # QR Code label
        qr_label = tk.Label(
            qr_frame,
            text="QR Code:",
            bg='#E3EDF7',
            fg='#2F4F7F',
            font=('Arial', 14, 'bold')
        )
        qr_label.pack()
        
        # QR Code image or placeholder
        if self.vehicle['has_qr']:
            self.create_qr_display(qr_frame)
        else:
            na_label = tk.Label(
                qr_frame,
                text="N/A",
                bg='#E3EDF7',
                fg='#666666',
                font=('Arial', 12),
                pady=10
            )
            na_label.pack()
            
    def create_qr_display(self, parent):
        """Create QR code display with simulated QR image"""
        # QR code container
        qr_container = tk.Frame(parent, bg='#E3EDF7', pady=10)
        qr_container.pack()
        
        # Simulated QR code (using a frame with pattern)
        qr_simulated = tk.Frame(
            qr_container,
            bg='white',
            width=120,
            height=120,
            relief='solid',
            bd=1
        )
        qr_simulated.pack()
        qr_simulated.pack_propagate(False)
        
        # Create a simple QR-like pattern using labels
        self.create_qr_pattern(qr_simulated)
        
        # QR code info text
        info_text = tk.Label(
            qr_container,
            text=f"Scan for vehicle {self.vehicle['plate_number']}",
            bg='#E3EDF7',
            fg='#2F4F7F',
            font=('Arial', 10),
            pady=(5, 0)
        )
        info_text.pack()
        
    def create_qr_pattern(self, parent):
        """Create a simple QR-like pattern for visualization"""
        # This creates a simple pattern that looks somewhat like a QR code
        colors = ['black', 'white']
        for i in range(8):
            row_frame = tk.Frame(parent, bg='white')
            row_frame.pack(fill=tk.BOTH, expand=True)
            
            for j in range(8):
                # Create a pattern with alternating colors
                color = colors[(i + j) % 2]
                if (i < 2 and j < 2) or (i < 2 and j > 5) or (i > 5 and j < 2):
                    color = 'black'  # QR position markers
                
                pixel = tk.Frame(
                    row_frame,
                    bg=color,
                    width=15,
                    height=15
                )
                pixel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
    def create_back_button(self, parent):
        """Create back to dashboard button"""
        back_btn = tk.Button(
            parent,
            text="← Back to Dashboard",
            bg='#5284BD',
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            command=self.back_to_dashboard,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        back_btn.pack(pady=(20, 0))
        
        # Bind hover effects
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg='#3D6A9F'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg='#5284BD'))
        
    def back_to_dashboard(self):
        """Handle back to dashboard action"""
        if messagebox.askyesno("Confirm", "Return to Dashboard?"):
            self.root.quit()

    def create_action_buttons(self, parent):
        """Create additional action buttons based on vehicle status"""
        if self.vehicle['status'] == 'active':
            action_frame = tk.Frame(parent, bg='#E3EDF7')
            action_frame.pack(fill=tk.X, pady=(10, 0))
            
            # Remove vehicle button
            remove_btn = tk.Button(
                action_frame,
                text="🚗 Remove Vehicle",
                bg='#e74c3c',
                fg='white',
                font=('Arial', 11, 'bold'),
                relief='flat',
                command=self.remove_vehicle,
                padx=15,
                pady=8
            )
            remove_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            # Generate QR button
            qr_btn = tk.Button(
                action_frame,
                text="📱 Generate QR",
                bg='#3498db',
                fg='white',
                font=('Arial', 11, 'bold'),
                relief='flat',
                command=self.generate_qr,
                padx=15,
                pady=8
            )
            qr_btn.pack(side=tk.LEFT)
            
            # Bind hover effects
            remove_btn.bind("<Enter>", lambda e: remove_btn.config(bg='#c0392b'))
            remove_btn.bind("<Leave>", lambda e: remove_btn.config(bg='#e74c3c'))
            qr_btn.bind("<Enter>", lambda e: qr_btn.config(bg='#2980b9'))
            qr_btn.bind("<Leave>", lambda e: qr_btn.config(bg='#3498db'))
            
    def remove_vehicle(self):
        """Handle vehicle removal"""
        if messagebox.askyesno(
            "Remove Vehicle", 
            f"Are you sure you want to remove vehicle {self.vehicle['plate_number']} from slot {self.vehicle['slot_number']}?"
        ):
            messagebox.showinfo(
                "Success", 
                f"Vehicle {self.vehicle['plate_number']} has been removed successfully!"
            )
            self.back_to_dashboard()
            
    def generate_qr(self):
        """Handle QR code generation"""
        messagebox.showinfo(
            "QR Code Generated", 
            f"QR code for vehicle {self.vehicle['plate_number']} has been generated!"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleDetailsApp(root)
    root.mainloop()