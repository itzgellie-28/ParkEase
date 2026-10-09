MAX_PARKING_SLOTS = 50

class Vehicle:
    def __init__(self, plate_number="", vehicle_type="", time_in=0, time_out=0, slot_number=0):
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.time_in = time_in
        self.time_out = time_out
        self.slot_number = slot_number

def calculate_fee(vehicle_type, hours):
    if vehicle_type.lower() == "car":
        return hours * 20
    elif vehicle_type.lower() == "motorcycle":
        return hours * 15
    else:
        return hours * 25
