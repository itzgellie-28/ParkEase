from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from datetime import datetime, timedelta
from parksystem import generate_qr
from parking_system import calculate_fee
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = "replace-with-your-secret-key"

# MySQL Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parking_db"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

# User types
USER_TYPES = {
    'admin': 'admin',
    'staff': 'staff'
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first.", "error")
            return redirect(url_for('login'))
        if session.get('user_type') != USER_TYPES['admin']:
            flash("Admin access required.", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Staff required decorator
def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first.", "error")
            return redirect(url_for('login'))
        if session.get('user_type') != USER_TYPES['staff']:
            flash("Staff access required.", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Cleanup old history
def cleanup_old_history(days=30):
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        cutoff = datetime.now() - timedelta(days=days)
        sql = "DELETE FROM vehicles WHERE time_out IS NOT NULL AND time_out < %s"
        cursor.execute(sql, (cutoff,))
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Cleanup error: {e}")
    finally:
        conn.close()

# ADMIN SIGNUP (Only for creating first admin)
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('login'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Check if any admin exists
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE user_type=%s", (USER_TYPES['admin'],))
        admin_count = cursor.fetchone()['count']
        
        if admin_count > 0:
            flash("Admin registration is closed. Please contact existing admin.", "error")
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            secret_key = request.form['secret_key']

            if secret_key != "admin123":
                flash("Invalid admin secret key!", "error")
                return redirect(url_for('admin_signup'))

            if password != confirm_password:
                flash("Passwords do not match!", "error")
                return redirect(url_for('admin_signup'))

            hashed_password = generate_password_hash(password)
            try:
                cursor.execute("INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)", 
                              (username, hashed_password, USER_TYPES['admin']))
                conn.commit()
                flash("Admin account created successfully! You can now login.", "success")
                return redirect(url_for('login'))
            except mysql.connector.IntegrityError:
                flash("Username already exists!", "error")
                return redirect(url_for('admin_signup'))

        return render_template('admin_signup.py')
    finally:
        conn.close()

# STAFF SIGNUP (Admin only)
@app.route('/staff/signup', methods=['GET', 'POST'])
@admin_required
def staff_signup():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash("Passwords do not match!", "error")
                return redirect(url_for('staff_signup'))

            hashed_password = generate_password_hash(password)
            try:
                cursor.execute("INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)", 
                              (username, hashed_password, USER_TYPES['staff']))
                conn.commit()
                flash("Staff account created successfully!", "success")
                return redirect(url_for('manage_staff'))
            except mysql.connector.IntegrityError:
                flash("Username already exists!", "error")
                return redirect(url_for('staff_signup'))

        return render_template('staff_signup.py')
    finally:
        conn.close()

# LOGIN (for both admin and staff)
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("=" * 50)
    print("🔐 LOGIN ROUTE ACCESSED")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        print("❌ DATABASE CONNECTION FAILED")
        flash("Database connection failed!", "error")
        return render_template('login.py', user_types=USER_TYPES)
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check current users
        cursor.execute("SELECT id, username, user_type, created_at FROM users")
        all_users = cursor.fetchall()
        print(f"📋 CURRENT USERS IN DATABASE: {all_users}")
        
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            user_type = request.form.get('user_type', 'staff')
            
            print(f"🔑 LOGIN ATTEMPT:")
            print(f"   Username: '{username}'")
            print(f"   Password: {'*' * len(password)}")
            print(f"   User Type: '{user_type}'")
            print(f"   Form data: {request.form}")
            
            if not username or not password:
                print("❌ MISSING USERNAME OR PASSWORD")
                flash("Please enter both username and password!", "error")
                return render_template('login.py', user_types=USER_TYPES)

            # Check if user exists with detailed debugging
            print(f"🔍 SEARCHING FOR USER: username='{username}', user_type='{user_type}'")
            cursor.execute("SELECT * FROM users WHERE username=%s AND user_type=%s", (username, user_type))
            user = cursor.fetchone()
            
            if user:
                print(f"✅ USER FOUND: {user}")
                print(f"   User ID: {user['id']}")
                print(f"   Username: {user['username']}")
                print(f"   User Type: {user['user_type']}")
                print(f"   Password hash: {user['password'][:30]}...")
                
                # Verify password
                print(f"🔐 VERIFYING PASSWORD...")
                password_correct = check_password_hash(user['password'], password)
                print(f"   Password correct: {password_correct}")
                
                if password_correct:
                    # Set session
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['user_type'] = user['user_type']
                    session.permanent = False
                    
                    print(f"🎉 LOGIN SUCCESSFUL!")
                    print(f"   Session set - User ID: {session['user_id']}")
                    print(f"   Redirecting to dashboard...")
                    
                    flash(f"Login successful! Welcome {user_type}.", "success")
                    return redirect(url_for('dashboard'))
                else:
                    print("❌ PASSWORD VERIFICATION FAILED")
                    # Debug: Let's see what the actual password should be
                    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
                    actual_hash = cursor.fetchone()['password']
                    print(f"   Stored hash: {actual_hash}")
                    print(f"   Input password: {password}")
                    flash("Invalid password!", "error")
            else:
                print(f"❌ USER NOT FOUND")
                print(f"   No user found with username='{username}' and type='{user_type}'")
                print(f"   Available users: {all_users}")
                flash("Invalid username or user type!", "error")
        
        return render_template('login.py', user_types=USER_TYPES)
        
    except Exception as e:
        print(f"💥 LOGIN ERROR: {str(e)}")
        import traceback
        print("TRACEBACK:")
        traceback.print_exc()
        flash(f"Login error: {str(e)}", "error")
        return render_template('login.py', user_types=USER_TYPES)
    finally:
        if conn and conn.is_connected():
            conn.close()
            print("✅ DATABASE CONNECTION CLOSED")
    print("=" * 50)

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

# DASHBOARD
@app.route('/')
@login_required
def dashboard():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return render_template('dashboard.py', vehicles=[], available_slots=50, occupied_slots=0, user_type=session.get('user_type'), current_date=datetime.now().strftime('%Y-%m-%d'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Get active vehicles with staff information
        cursor.execute("""
            SELECT v.*, u.username as staff_in 
            FROM vehicles v 
            LEFT JOIN users u ON v.staff_id = u.id 
            WHERE v.time_out IS NULL 
            ORDER BY v.slot_number
        """)
        vehicles = cursor.fetchall()
        
        # Calculate available slots (50 total slots)
        total_slots = 50
        occupied_slots = len(vehicles)
        available_slots = total_slots - occupied_slots
        
        user_type = session.get('user_type')
        
        # Format time for display
        for v in vehicles:
            if isinstance(v['time_in'], datetime):
                v['time_in'] = v['time_in'].strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"📊 Dashboard - Vehicles: {len(vehicles)}, QR codes: {[v.get('qr_code_file', 'No QR') for v in vehicles]}")
        
        return render_template('dashboard.html', 
                             vehicles=vehicles,
                             available_slots=available_slots,
                             occupied_slots=occupied_slots,
                             user_type=user_type,
                             current_date=datetime.now().strftime('%Y-%m-%d'))
    finally:
        conn.close()
        
# PARK VEHICLE (Staff only)
@app.route('/park', methods=['GET', 'POST'])
@staff_required
def park_vehicle():
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed!", "error")
            return redirect(url_for('park_vehicle'))
        
        try:
            cursor = conn.cursor(dictionary=True)
            plate = request.form['plate_number']
            vtype = request.form['vehicle_type']
            slot = int(request.form['slot_number'])
            time_in = datetime.now()

            # Check if slot is already occupied
            cursor.execute("SELECT * FROM vehicles WHERE slot_number=%s AND time_out IS NULL", (slot,))
            if cursor.fetchone():
                flash(f"Slot {slot} is already occupied!", "error")
                return redirect(url_for('park_vehicle'))

            # Ensure static directory exists
            os.makedirs('static', exist_ok=True)
            
            print(f"🔄 Generating QR code for vehicle: {plate}")
            qr_filename = generate_qr(plate, vtype, slot, time_in)
            print(f"✅ QR code generated: {qr_filename}")

            sql = """
            INSERT INTO vehicles (plate_number, vehicle_type, time_in, slot_number, qr_code_file, staff_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (plate, vtype, time_in, slot, qr_filename, session['user_id']))
            conn.commit()
            
            print(f"✅ Vehicle parked successfully with QR code: {qr_filename}")
            flash("Vehicle parked successfully! QR code generated.", "success")
            return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"❌ Error parking vehicle: {str(e)}")
            flash(f"Error parking vehicle: {str(e)}", "error")
            return redirect(url_for('park_vehicle'))
        finally:
            conn.close()

    return render_template('park_form.py')

# REMOVE VEHICLE (Staff only)
@app.route('/remove/<int:vehicle_id>', methods=['POST'])
@staff_required
def remove_vehicle(vehicle_id):
    print(f"🚗🔍 REMOVE VEHICLE ROUTE CALLED")
    print(f"📝 Vehicle ID: {vehicle_id}")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            print("❌ VEHICLE NOT FOUND IN DATABASE")
            flash("Vehicle not found.", "error")
            return redirect(url_for('dashboard'))
        
        print(f"✅ Vehicle found: {vehicle}")
        
        time_out = datetime.now()
        
        # Calculate hours parked and fee
        time_in = vehicle['time_in']
        if isinstance(time_in, str):
            time_in = datetime.strptime(time_in, '%Y-%m-%d %H:%M:%S')
        
        time_diff = time_out - time_in
        hours = max(1, time_diff.seconds // 3600)
        fee = calculate_fee(vehicle['vehicle_type'], hours)
        
        print(f"💰 Hours parked: {hours}")
        print(f"💰 Calculated fee: ₱{fee}")
        
        # Update vehicle record
        cursor.execute("UPDATE vehicles SET time_out=%s, fee=%s, staff_id_out=%s WHERE id=%s", 
                      (time_out, fee, session['user_id'], vehicle_id))
        
        conn.commit()
        
        print("✅ VEHICLE SUCCESSFULLY REMOVED FROM DATABASE")
        flash(f"Vehicle {vehicle['plate_number']} removed. Fee: ₱{fee}", "success")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        flash(f"Error removing vehicle: {str(e)}", "error")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('dashboard'))

# RESTORE VEHICLE (Admin only)
@app.route('/restore/<int:vehicle_id>', methods=['POST'])
@admin_required
def restore_vehicle(vehicle_id):
    print(f"🔄 RESTORE VEHICLE ROUTE CALLED")
    print(f"📝 Vehicle ID: {vehicle_id}")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('history'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            print("❌ VEHICLE NOT FOUND IN DATABASE")
            flash("Vehicle not found.", "error")
            return redirect(url_for('history'))
        
        print(f"✅ Vehicle found: {vehicle}")
        
        # Restore vehicle by setting time_out and fee to NULL
        cursor.execute("UPDATE vehicles SET time_out = NULL, fee = NULL, staff_id_out = NULL WHERE id=%s", (vehicle_id,))
        conn.commit()
        
        print("✅ VEHICLE SUCCESSFULLY RESTORED")
        flash(f"Vehicle {vehicle['plate_number']} restored to active list.", "success")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        flash(f"Error restoring vehicle: {str(e)}", "error")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('history'))

# DELETE VEHICLE (Admin only)
@app.route('/delete/<int:vehicle_id>', methods=['POST'])
@admin_required
def delete_vehicle(vehicle_id):
    print(f"🗑️ DELETE VEHICLE ROUTE CALLED")
    print(f"📝 Vehicle ID: {vehicle_id}")
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('history'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            print("❌ VEHICLE NOT FOUND IN DATABASE")
            flash("Vehicle not found.", "error")
            return redirect(url_for('history'))
        
        print(f"✅ Vehicle found: {vehicle}")
        
        # Permanently delete the vehicle record
        cursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
        conn.commit()
        
        print("✅ VEHICLE RECORD PERMANENTLY DELETED")
        flash(f"Vehicle record for {vehicle['plate_number']} permanently deleted.", "success")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        flash(f"Error deleting vehicle: {str(e)}", "error")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('history'))

# HISTORY (Admin can see all, Staff see limited)
@app.route('/history')
@login_required
def history():
    cleanup_old_history(days=30)
    
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return render_template('history.html', vehicles=[], user_type=session.get('user_type'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        user_type = session.get('user_type')
        if user_type == USER_TYPES['admin']:
            # Admin can see all history
            cursor.execute("""
                SELECT v.*, u_in.username as staff_in, u_out.username as staff_out 
                FROM vehicles v
                LEFT JOIN users u_in ON v.staff_id = u_in.id
                LEFT JOIN users u_out ON v.staff_id_out = u_out.id
                WHERE time_out IS NOT NULL 
                ORDER BY time_out DESC
            """)
        else:
            # Staff can only see recent history (last 7 days)
            week_ago = datetime.now() - timedelta(days=7)
            cursor.execute("""
                SELECT v.*, u_in.username as staff_in, u_out.username as staff_out 
                FROM vehicles v
                LEFT JOIN users u_in ON v.staff_id = u_in.id
                LEFT JOIN users u_out ON v.staff_id_out = u_out.id
                WHERE time_out IS NOT NULL AND time_out >= %s 
                ORDER BY time_out DESC
            """, (week_ago,))
        
        vehicles = cursor.fetchall()
        for v in vehicles:
            if isinstance(v['time_in'], datetime):
                v['time_in'] = v['time_in'].strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(v['time_out'], datetime):
                v['time_out'] = v['time_out'].strftime('%Y-%m-%d %H:%M:%S')
        
        return render_template('history.py', vehicles=vehicles, user_type=user_type)
    finally:
        conn.close()

# MANAGE STAFF (Admin only)
@app.route('/admin/staff')
@admin_required
def manage_staff():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return render_template('manage_staff.py', staff_members=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, created_at FROM users WHERE user_type=%s ORDER BY created_at DESC", 
                      (USER_TYPES['staff'],))
        staff_members = cursor.fetchall()
        return render_template('manage_staff.py', staff_members=staff_members)
    finally:
        conn.close()

# DELETE STAFF (Admin only)
@app.route('/admin/staff/delete/<int:staff_id>', methods=['POST'])
@admin_required
def delete_staff(staff_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('manage_staff'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Prevent admin from deleting themselves
        if staff_id == session.get('user_id'):
            flash("You cannot delete your own account!", "error")
            return redirect(url_for('manage_staff'))
        
        cursor.execute("DELETE FROM users WHERE id=%s AND user_type=%s", (staff_id, USER_TYPES['staff']))
        conn.commit()
        flash("Staff account deleted successfully.", "success")
        return redirect(url_for('manage_staff'))
    finally:
        conn.close()

# ADMIN REPORTS (Admin only)
@app.route('/admin/reports')
@admin_required
def admin_reports():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return render_template('admin_reports.py', 
                             activity_data=[], 
                             vehicle_stats=[], 
                             staff_activity=[],
                             current_date=datetime.now().strftime('%Y-%m-%d'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        # Get basic activity statistics
        cursor.execute("""
            SELECT DATE(time_out) as date, COUNT(*) as vehicles_processed
            FROM vehicles 
            WHERE time_out IS NOT NULL
            GROUP BY DATE(time_out) 
            ORDER BY date DESC 
            LIMIT 30
        """)
        activity_data = cursor.fetchall()
        
        # Get vehicle type statistics
        cursor.execute("""
            SELECT vehicle_type, COUNT(*) as count
            FROM vehicles 
            WHERE time_out IS NOT NULL
            GROUP BY vehicle_type
        """)
        vehicle_stats = cursor.fetchall()
        
        # Get staff activity
        cursor.execute("""
            SELECT u.username, 
                   COUNT(v.id) as vehicles_processed
            FROM users u
            LEFT JOIN vehicles v ON u.id = v.staff_id_out
            WHERE u.user_type = 'staff' AND v.time_out IS NOT NULL
            GROUP BY u.id, u.username
            ORDER BY vehicles_processed DESC
        """)
        staff_activity = cursor.fetchall()
        
        return render_template('admin_reports.py', 
                             activity_data=activity_data,
                             vehicle_stats=vehicle_stats,
                             staff_activity=staff_activity,
                             current_date=datetime.now().strftime('%Y-%m-%d'))
    finally:
        conn.close()

# SLOTS (Both admin and staff can view)
@app.route('/slots')
@login_required
def show_slots():
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return render_template('slots.py', slots=[], user_type=session.get('user_type'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT slot_number, plate_number, vehicle_type FROM vehicles WHERE time_out IS NULL")
        occupied = cursor.fetchall()
        occupied_map = {v['slot_number']: v for v in occupied}

        slots = []
        for i in range(1, 51):
            if i in occupied_map:
                slots.append({
                    'slot_number': i,
                    'status': 'occupied',
                    'plate': occupied_map[i]['plate_number'],
                    'vehicle_type': occupied_map[i]['vehicle_type']
                })
            else:
                slots.append({
                    'slot_number': i,
                    'status': 'available',
                    'plate': '',
                    'vehicle_type': ''
                })

        user_type = session.get('user_type')
        return render_template('slots.py', slots=slots, user_type=user_type)
    finally:
        conn.close()

# VEHICLE DETAILS (Both admin and staff can view)
@app.route('/vehicle/<int:vehicle_id>')
@login_required
def vehicle_detail(vehicle_id):
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed!", "error")
        return redirect(url_for('dashboard'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, u_in.username as staff_in, u_out.username as staff_out 
            FROM vehicles v
            LEFT JOIN users u_in ON v.staff_id = u_in.id
            LEFT JOIN users u_out ON v.staff_id_out = u_out.id
            WHERE v.id=%s
        """, (vehicle_id,))
        vehicle = cursor.fetchone()
        
        if not vehicle:
            flash("Vehicle not found!", "error")
            return redirect(url_for('dashboard'))

        # Format datetime for display
        if isinstance(vehicle['time_in'], datetime):
            vehicle['time_in'] = vehicle['time_in'].strftime('%Y-%m-%d %H:%M:%S')
        
        if vehicle['time_out'] and isinstance(vehicle['time_out'], datetime):
            vehicle['time_out'] = vehicle['time_out'].strftime('%Y-%m-%d %H:%M:%S')
        
        user_type = session.get('user_type')
        return render_template('vehicle_details.py', vehicle=vehicle, user_type=user_type)
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)