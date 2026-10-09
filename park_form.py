import tkinter as tk
from tkinter import ttk, messagebox
import random

class ParkVehicleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Park Vehicle - MallPark")
        self.root.geometry("600x500")
        self.root.configure(bg='#f8f9fa')
        
        # Center the window
        self.center_window()
        
        # Sample data for available slots
        self.available_slots = list(range(1, 51))
        
        # Flash messages storage
        self.flash_messages = []
        
        self.setup_ui()
        
    def center_window(self):
        self.root.update_idletasks()
        width = 600
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f8f9fa', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Park Vehicle",
            bg='#f8f9fa',
            fg='#212529',
            font=('Segoe UI', 24, 'bold'),
            pady=10
        )
        title_label.pack(anchor='w')
        
        # Flash messages area
        self.flash_frame = tk.Frame(main_frame, bg='#f8f9fa')
        self.flash_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add sample flash message (you can remove this in production)
        # self.add_flash_message("Vehicle parked successfully!", "success")
        
        # Card container (form)
        self.create_form_card(main_frame)
        
    def create_form_card(self, parent):
        # Card frame
        card_frame = tk.Frame(
            parent,
            bg='white',
            relief='raised',
            bd=1,
            padx=25,
            pady=25
        )
        card_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form content
        self.create_form_fields(card_frame)
        
    def create_form_fields(self, parent):
        # Plate Number
        plate_frame = tk.Frame(parent, bg='white')
        plate_frame.pack(fill=tk.X, pady=(0, 20))
        
        plate_label = tk.Label(
            plate_frame,
            text="Plate Number",
            bg='white',
            fg='#212529',
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        plate_label.pack(fill=tk.X, pady=(0, 5))
        
        self.plate_entry = tk.Entry(
            plate_frame,
            font=('Segoe UI', 12),
            relief='solid',
            bd=1,
            bg='white'
        )
        self.plate_entry.pack(fill=tk.X, ipady=8)
        self.plate_entry.focus()
        
        # Vehicle Type
        vehicle_frame = tk.Frame(parent, bg='white')
        vehicle_frame.pack(fill=tk.X, pady=(0, 20))
        
        vehicle_label = tk.Label(
            vehicle_frame,
            text="Vehicle Type",
            bg='white',
            fg='#212529',
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        vehicle_label.pack(fill=tk.X, pady=(0, 5))
        
        self.vehicle_var = tk.StringVar()
        vehicle_combo = ttk.Combobox(
            vehicle_frame,
            textvariable=self.vehicle_var,
            values=["Select Vehicle Type", "Car", "Motorcycle", "Other"],
            state="readonly",
            font=('Segoe UI', 12)
        )
        vehicle_combo.pack(fill=tk.X, ipady=8)
        vehicle_combo.current(0)
        
        # Slot Number
        slot_frame = tk.Frame(parent, bg='white')
        slot_frame.pack(fill=tk.X, pady=(0, 30))
        
        slot_label = tk.Label(
            slot_frame,
            text="Slot Number (1-50)",
            bg='white',
            fg='#212529',
            font=('Segoe UI', 11, 'bold'),
            anchor='w'
        )
        slot_label.pack(fill=tk.X, pady=(0, 5))
        
        # Frame for slot input and available slots
        slot_input_frame = tk.Frame(slot_frame, bg='white')
        slot_input_frame.pack(fill=tk.X)
        
        self.slot_var = tk.StringVar()
        slot_spinbox = tk.Spinbox(
            slot_input_frame,
            from_=1,
            to=50,
            textvariable=self.slot_var,
            font=('Segoe UI', 12),
            width=10,
            relief='solid',
            bd=1
        )
        slot_spinbox.pack(side=tk.LEFT)
        
        # Available slots info
        available_label = tk.Label(
            slot_input_frame,
            text=f"Available slots: {len(self.available_slots)}",
            bg='white',
            fg='#6c757d',
            font=('Segoe UI', 10),
            padx=10
        )
        available_label.pack(side=tk.LEFT)
        
        # Quick slot selection buttons
        self.create_quick_slots(slot_frame)
        
        # Buttons
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Park Vehicle button
        park_btn = tk.Button(
            button_frame,
            text="🚗 Park Vehicle",
            bg='#198754',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            command=self.park_vehicle,
            padx=20,
            pady=10
        )
        park_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="❌ Cancel",
            bg='#6c757d',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief='flat',
            command=self.cancel,
            padx=20,
            pady=10
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Bind hover effects
        park_btn.bind("<Enter>", lambda e: park_btn.config(bg='#157347'))
        park_btn.bind("<Leave>", lambda e: park_btn.config(bg='#198754'))
        
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg='#5c636a'))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg='#6c757d'))
        
    def create_quick_slots(self, parent):
        """Create quick slot selection buttons"""
        quick_frame = tk.Frame(parent, bg='white')
        quick_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            quick_frame,
            text="Quick select:",
            bg='white',
            fg='#6c757d',
            font=('Segoe UI', 10),
            anchor='w'
        ).pack(side=tk.LEFT)
        
        # Show 5 random available slots as quick buttons
        quick_slots = random.sample(self.available_slots, min(5, len(self.available_slots)))
        
        for slot in quick_slots:
            slot_btn = tk.Button(
                quick_frame,
                text=str(slot),
                bg='#0d6efd',
                fg='white',
                font=('Segoe UI', 9),
                relief='flat',
                command=lambda s=slot: self.select_slot(s),
                padx=8,
                pady=4
            )
            slot_btn.pack(side=tk.LEFT, padx=(5, 0))
            
            # Bind hover effects
            slot_btn.bind("<Enter>", lambda e, b=slot_btn: b.config(bg='#0b5ed7'))
            slot_btn.bind("<Leave>", lambda e, b=slot_btn: b.config(bg='#0d6efd'))
        
    def select_slot(self, slot_number):
        """Select a slot from quick selection"""
        self.slot_var.set(str(slot_number))
        
    def add_flash_message(self, message, category):
        """Add a flash message to the display"""
        # Clear existing flash messages
        for widget in self.flash_frame.winfo_children():
            widget.destroy()
            
        # Determine colors based on category
        colors = {
            'success': ('#d1e7dd', '#0f5132', '#badbcc'),
            'error': ('#f8d7da', '#721c24', '#f5c6cb')
        }
        bg_color, fg_color, border_color = colors.get(category, ('#d1ecf1', '#0c5460', '#b8daff'))
        
        # Create message frame with border
        message_frame = tk.Frame(
            self.flash_frame,
            bg=border_color,
            padx=1,
            pady=1
        )
        message_frame.pack(fill=tk.X)
        
        message_label = tk.Label(
            message_frame,
            text=message,
            bg=bg_color,
            fg=fg_color,
            font=('Segoe UI', 10),
            padx=12,
            pady=10,
            justify=tk.LEFT
        )
        message_label.pack(fill=tk.X)
        
        # Auto-hide after 5 seconds
        self.root.after(5000, lambda: message_frame.pack_forget())
        
    def park_vehicle(self):
        """Handle vehicle parking"""
        plate_number = self.plate_entry.get().strip().upper()
        vehicle_type = self.vehicle_var.get()
        slot_number = self.slot_var.get()
        
        # Validation
        if not plate_number:
            messagebox.showerror("Error", "Please enter a plate number")
            self.plate_entry.focus()
            return
            
        if vehicle_type == "Select Vehicle Type":
            messagebox.showerror("Error", "Please select a vehicle type")
            return
            
        if not slot_number:
            messagebox.showerror("Error", "Please enter a slot number")
            return
            
        try:
            slot_num = int(slot_number)
            if slot_num < 1 or slot_num > 50:
                messagebox.showerror("Error", "Slot number must be between 1 and 50")
                return
                
            if slot_num not in self.available_slots:
                messagebox.showerror("Error", f"Slot {slot_num} is not available")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid slot number")
            return
            
        # Simulate parking process
        self.simulate_parking(plate_number, vehicle_type, slot_num)
        
    def simulate_parking(self, plate_number, vehicle_type, slot_number):
        """Simulate the parking process with loading state"""
        # Disable form
        self.set_form_state('disabled')
        
        # Update button to show loading
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn in child.winfo_children():
                            if isinstance(btn, tk.Button) and "Park Vehicle" in btn.cget('text'):
                                btn.config(text="🔄 Parking...", state='disabled')
                                break
        
        # Simulate processing delay
        self.root.after(2000, lambda: self.complete_parking(plate_number, vehicle_type, slot_number))
        
    def complete_parking(self, plate_number, vehicle_type, slot_number):
        """Complete the parking process"""
        # Remove slot from available
        if slot_number in self.available_slots:
            self.available_slots.remove(slot_number)
        
        # Show success message
        success_msg = f"Vehicle {plate_number} ({vehicle_type}) parked successfully in slot {slot_number}!"
        self.add_flash_message(success_msg, "success")
        
        # Reset form
        self.reset_form()
        
        # Re-enable form
        self.set_form_state('normal')
        
        # Show confirmation dialog
        messagebox.showinfo("Success", success_msg)
        
    def set_form_state(self, state):
        """Enable or disable form elements"""
        state_bool = state == 'normal'
        self.plate_entry.config(state=state)
        # Note: Combobox state handling is different in tkinter
        
    def reset_form(self):
        """Reset the form to initial state"""
        self.plate_entry.delete(0, tk.END)
        self.vehicle_var.set("Select Vehicle Type")
        self.slot_var.set("")
        
        # Reset button text
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn in child.winfo_children():
                            if isinstance(btn, tk.Button) and "Parking..." in btn.cget('text'):
                                btn.config(text="🚗 Park Vehicle", state='normal')
                                break
        
    def cancel(self):
        """Handle cancel action"""
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel? Any unsaved data will be lost."):
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkVehicleApp(root)
    root.mainloop()