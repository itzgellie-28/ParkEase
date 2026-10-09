import tkinter as tk
from tkinter import ttk, messagebox
import random

class ParkingSlotsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Slots - MallPark")
        self.root.geometry("1000x700")
        self.root.configure(bg='#eef2f7')
        
        # Center the window
        self.center_window()
        
        # Generate sample slot data
        self.slots = self.generate_sample_slots()
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 1000
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def generate_sample_slots(self):
        """Generate sample slot data with random occupancy"""
        slots = []
        for i in range(1, 51):
            # Randomly assign occupancy (about 30% occupied)
            is_occupied = random.random() < 0.3
            
            if is_occupied:
                # Generate random plate number
                letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
                numbers = ''.join(random.choices('0123456789', k=3))
                plate = f"{letters}{numbers}"
                
                # Random vehicle type
                vehicle_types = ['Car', 'Motorcycle', 'Truck']
                vehicle_type = random.choice(vehicle_types)
                
                slots.append({
                    'slot_number': i,
                    'status': 'occupied',
                    'plate': plate,
                    'vehicle_type': vehicle_type
                })
            else:
                slots.append({
                    'slot_number': i,
                    'status': 'available',
                    'plate': '',
                    'vehicle_type': ''
                })
        return slots
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#eef2f7', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Back button
        self.create_back_button(main_frame)
        
        # Title
        self.create_title(main_frame)
        
        # Parking slots grid
        self.create_slots_grid(main_frame)
        
        # Statistics footer
        self.create_statistics_footer(main_frame)
        
    def create_back_button(self, parent):
        back_btn = tk.Button(
            parent,
            text="← Back to Dashboard",
            bg='#5284BD',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='flat',
            command=self.back_to_dashboard,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        back_btn.pack(anchor='w', pady=(0, 20))
        
        # Bind hover effects
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg='#3D6A9F'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg='#5284BD'))
        
    def create_title(self, parent):
        title_label = tk.Label(
            parent,
            text="Parking Slot Viewer",
            bg='#eef2f7',
            fg='#2c3e50',
            font=('Arial', 20, 'bold'),
            pady=10
        )
        title_label.pack()
        
    def create_slots_grid(self, parent):
        # Create a frame for the grid with scrollbar
        grid_container = tk.Frame(parent, bg='#eef2f7')
        grid_container.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Create a canvas and scrollbar for the grid
        canvas = tk.Canvas(grid_container, bg='#eef2f7', highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_container, orient="vertical", command=canvas.yview)
        
        # Grid frame that will hold the slots
        self.grid_frame = tk.Frame(canvas, bg='#eef2f7')
        
        # Configure canvas scrolling
        self.grid_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create the slots grid
        self.create_slots()
        
        # Bind mouse wheel to canvas
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def create_slots(self):
        """Create the parking slots grid"""
        # Configure grid layout - 10 columns
        for i in range(10):
            self.grid_frame.columnconfigure(i, weight=1, uniform="slot_col")
        
        # Create slots in grid
        for i, slot in enumerate(self.slots):
            row = i // 10
            col = i % 10
            
            # Determine slot colors based on status
            if slot['status'] == 'available':
                bg_color = '#9CB8D9'  # Light pastel blue
                fg_color = '#2c3e50'
            else:
                bg_color = '#3D6A9F'  # Dark pastel blue
                fg_color = 'white'
            
            # Create slot frame
            slot_frame = tk.Frame(
                self.grid_frame,
                bg=bg_color,
                relief='raised',
                bd=1,
                padx=5,
                pady=5,
                width=80,
                height=80
            )
            slot_frame.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
            slot_frame.pack_propagate(False)
            
            # Slot number
            slot_number_label = tk.Label(
                slot_frame,
                text=f"Slot {slot['slot_number']}",
                bg=bg_color,
                fg=fg_color,
                font=('Arial', 10, 'bold')
            )
            slot_number_label.pack(pady=(5, 0))
            
            # Slot details
            if slot['status'] == 'occupied':
                # Plate number
                plate_label = tk.Label(
                    slot_frame,
                    text=f"Plate: {slot['plate']}",
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 7)
                )
                plate_label.pack()
                
                # Vehicle type
                type_label = tk.Label(
                    slot_frame,
                    text=f"Type: {slot['vehicle_type']}",
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 7)
                )
                type_label.pack()
            else:
                # Available text
                available_label = tk.Label(
                    slot_frame,
                    text="Available",
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 8)
                )
                available_label.pack(expand=True)
            
            # Bind click event for slot details
            slot_frame.bind("<Button-1>", lambda e, s=slot: self.show_slot_details(s))
            
            # Bind hover effects
            slot_frame.bind("<Enter>", lambda e, f=slot_frame: self.on_slot_enter(f))
            slot_frame.bind("<Leave>", lambda e, f=slot_frame, bg=bg_color: self.on_slot_leave(f, bg))
    
    def on_slot_enter(self, slot_frame):
        """Handle mouse enter on slot"""
        slot_frame.configure(relief='sunken')
        
    def on_slot_leave(self, slot_frame, original_bg):
        """Handle mouse leave on slot"""
        slot_frame.configure(relief='raised')
        
    def show_slot_details(self, slot):
        """Show detailed information about a slot"""
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Slot {slot['slot_number']} Details")
        details_window.geometry("300x200")
        details_window.configure(bg='#eef2f7')
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Center the details window
        details_window.update_idletasks()
        x = (details_window.winfo_screenwidth() // 2) - (300 // 2)
        y = (details_window.winfo_screenheight() // 2) - (200 // 2)
        details_window.geometry(f'300x200+{x}+{y}')
        
        # Header
        header_bg = '#3D6A9F' if slot['status'] == 'occupied' else '#9CB8D9'
        header_fg = 'white' if slot['status'] == 'occupied' else '#2c3e50'
        
        header_frame = tk.Frame(details_window, bg=header_bg, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"Slot {slot['slot_number']}",
            bg=header_bg,
            fg=header_fg,
            font=('Arial', 16, 'bold')
        ).pack(expand=True)
        
        # Content
        content_frame = tk.Frame(details_window, bg='#eef2f7', padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status
        status_frame = tk.Frame(content_frame, bg='#eef2f7')
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            status_frame,
            text="Status:",
            bg='#eef2f7',
            fg='#2c3e50',
            font=('Arial', 11, 'bold'),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)
        
        status_text = "Occupied" if slot['status'] == 'occupied' else "Available"
        status_color = '#e74c3c' if slot['status'] == 'occupied' else '#27ae60'
        
        tk.Label(
            status_frame,
            text=status_text,
            bg='#eef2f7',
            fg=status_color,
            font=('Arial', 11, 'bold'),
            anchor='w'
        ).pack(side=tk.LEFT)
        
        if slot['status'] == 'occupied':
            # Plate number
            plate_frame = tk.Frame(content_frame, bg='#eef2f7')
            plate_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                plate_frame,
                text="Plate:",
                bg='#eef2f7',
                fg='#2c3e50',
                font=('Arial', 11, 'bold'),
                width=10,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                plate_frame,
                text=slot['plate'],
                bg='#eef2f7',
                fg='#2c3e50',
                font=('Arial', 11),
                anchor='w'
            ).pack(side=tk.LEFT)
            
            # Vehicle type
            type_frame = tk.Frame(content_frame, bg='#eef2f7')
            type_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                type_frame,
                text="Type:",
                bg='#eef2f7',
                fg='#2c3e50',
                font=('Arial', 11, 'bold'),
                width=10,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                type_frame,
                text=slot['vehicle_type'],
                bg='#eef2f7',
                fg='#2c3e50',
                font=('Arial', 11),
                anchor='w'
            ).pack(side=tk.LEFT)
        
        # Close button
        button_frame = tk.Frame(content_frame, bg='#eef2f7', pady=10)
        button_frame.pack(fill=tk.X)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            bg='#5284BD',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief='flat',
            command=details_window.destroy,
            padx=20,
            pady=5
        )
        close_btn.pack()
        
        # Bind hover effects
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg='#3D6A9F'))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg='#5284BD'))
        
    def create_statistics_footer(self, parent):
        """Create statistics footer showing slot usage"""
        stats_frame = tk.Frame(parent, bg='#eef2f7', pady=10)
        stats_frame.pack(fill=tk.X)
        
        # Calculate statistics
        total_slots = len(self.slots)
        occupied_slots = len([s for s in self.slots if s['status'] == 'occupied'])
        available_slots = total_slots - occupied_slots
        
        # Statistics labels
        stats_text = f"Total: {total_slots} | Available: {available_slots} | Occupied: {occupied_slots}"
        
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            bg='#eef2f7',
            fg='#2c3e50',
            font=('Arial', 11, 'bold')
        )
        stats_label.pack()
        
        # Refresh button
        refresh_btn = tk.Button(
            stats_frame,
            text="🔄 Refresh",
            bg='#27ae60',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            command=self.refresh_slots,
            padx=15,
            pady=5
        )
        refresh_btn.pack(pady=(10, 0))
        
        # Bind hover effects
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg='#219a52'))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg='#27ae60'))
        
    def refresh_slots(self):
        """Refresh the slots with new random data"""
        self.slots = self.generate_sample_slots()
        
        # Clear existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # Recreate slots
        self.create_slots()
        
        messagebox.showinfo("Refreshed", "Parking slots data has been refreshed!")
        
    def back_to_dashboard(self):
        """Handle back to dashboard action"""
        if messagebox.askyesno("Confirm", "Return to Dashboard?"):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingSlotsApp(root)
    root.mainloop()