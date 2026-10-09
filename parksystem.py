# parksystem.py
import qrcode
import os
from datetime import datetime

def generate_qr(plate_number, vehicle_type, slot_number, time_in):
    """
    Generate QR code for parked vehicle
    """
    try:
        # Create QR code data
        qr_data = f"""
Parking Information:
Plate: {plate_number}
Type: {vehicle_type}
Slot: {slot_number}
Time In: {time_in.strftime('%Y-%m-%d %H:%M:%S')}
        """.strip()
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_{plate_number}_{timestamp}.png"
        filepath = os.path.join('static', filename)
        
        # Save QR code
        qr_image.save(filepath)
        print(f"✅ QR code saved: {filepath}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error generating QR code: {e}")
        return None