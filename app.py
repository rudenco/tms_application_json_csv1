# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
import pandas as pd
import json
import os
import uuid
from datetime import datetime, date
from werkzeug.utils import secure_filename
import csv
from functools import wraps

app = Flask(__name__)
app.secret_key = 'tms_secret_key_2024'

# Configuration
DATA_DIR = "tms_data"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'json'}

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Data file paths
DRIVERS_FILE = os.path.join(DATA_DIR, "drivers.csv")
TRUCKS_FILE = os.path.join(DATA_DIR, "trucks.csv")
TRAILERS_FILE = os.path.join(DATA_DIR, "trailers.csv")
MAINTENANCE_FILE = os.path.join(DATA_DIR, "maintenance.csv")
OTR_FILE = os.path.join(DATA_DIR, "otr_repairs.csv")
PM_FILE = os.path.join(DATA_DIR, "pm_records.csv")
SHOP_JOBS_FILE = os.path.join(DATA_DIR, "shop_jobs.csv")


class TMSDataManager:
    def __init__(self):
        self.ensure_files_exist()

    def ensure_files_exist(self):
        """Create CSV files with headers if they don't exist"""

        # Drivers file
        if not os.path.exists(DRIVERS_FILE):
            drivers_df = pd.DataFrame(columns=[
                'driver_id', 'first_name', 'last_name', 'license_number',
                'driver_type', 'hire_date', 'phone', 'email', 'address',
                'cdl_expiry', 'medical_expiry', 'status', 'notes', 'created_at'
            ])
            drivers_df.to_csv(DRIVERS_FILE, index=False)

        # Trucks file
        if not os.path.exists(TRUCKS_FILE):
            trucks_df = pd.DataFrame(columns=[
                'truck_id', 'truck_number', 'make', 'model', 'year', 'vin',
                'engine_type', 'mileage', 'assigned_driver', 'status',
                'purchase_date', 'last_pm_date', 'next_pm_due', 'notes', 'created_at'
            ])
            trucks_df.to_csv(TRUCKS_FILE, index=False)

        # Trailers file
        if not os.path.exists(TRAILERS_FILE):
            trailers_df = pd.DataFrame(columns=[
                'trailer_id', 'trailer_number', 'type', 'year', 'make',
                'capacity', 'assigned_truck', 'status', 'last_inspection',
                'next_inspection_due', 'notes', 'created_at'
            ])
            trailers_df.to_csv(TRAILERS_FILE, index=False)

        # Maintenance file
        if not os.path.exists(MAINTENANCE_FILE):
            maintenance_df = pd.DataFrame(columns=[
                'maintenance_id', 'truck_id', 'trailer_id', 'maintenance_type',
                'date', 'mileage', 'description', 'parts_cost', 'labor_cost',
                'total_cost', 'shop_name', 'shop_location', 'technician',
                'status', 'notes', 'created_at'
            ])
            maintenance_df.to_csv(MAINTENANCE_FILE, index=False)

        # OTR Repairs file
        if not os.path.exists(OTR_FILE):
            otr_df = pd.DataFrame(columns=[
                'otr_id', 'truck_id', 'driver_id', 'breakdown_date', 'location',
                'issue_description', 'repair_shop', 'repair_cost', 'parts_used',
                'labor_hours', 'downtime_hours', 'tow_cost', 'hotel_cost',
                'total_cost', 'insurance_claim', 'status', 'notes', 'created_at'
            ])
            otr_df.to_csv(OTR_FILE, index=False)

        # PM Records file
        if not os.path.exists(PM_FILE):
            pm_df = pd.DataFrame(columns=[
                'pm_id', 'truck_id', 'pm_type', 'date', 'mileage', 'next_due_date',
                'next_due_mileage', 'shop_name', 'technician', 'oil_change',
                'filter_change', 'inspection_items', 'parts_cost', 'labor_cost',
                'total_cost', 'status', 'notes', 'created_at'
            ])
            pm_df.to_csv(PM_FILE, index=False)

        # Shop Jobs file
        if not os.path.exists(SHOP_JOBS_FILE):
            shop_jobs_df = pd.DataFrame(columns=[
                'job_id', 'truck_id', 'trailer_id', 'job_type', 'date_started',
                'date_completed', 'description', 'technician', 'parts_used',
                'labor_hours', 'parts_cost', 'labor_cost', 'total_cost',
                'status', 'priority', 'notes', 'created_at'
            ])
            shop_jobs_df.to_csv(SHOP_JOBS_FILE, index=False)

    def load_data(self, file_path):
        """Load data from CSV file"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading data from {file_path}: {str(e)}")
            return pd.DataFrame()

    def save_data(self, df, file_path):
        """Save data to CSV file"""
        try:
            df.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving data to {file_path}: {str(e)}")
            return False

    def generate_id(self):
        """Generate unique ID"""
        return str(uuid.uuid4())[:8]


# Initialize data manager
data_manager = TMSDataManager()


# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_dashboard_stats():
    """Get dashboard statistics"""
    drivers_df = data_manager.load_data(DRIVERS_FILE)
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trailers_df = data_manager.load_data(TRAILERS_FILE)
    maintenance_df = data_manager.load_data(MAINTENANCE_FILE)
    otr_df = data_manager.load_data(OTR_FILE)
    pm_df = data_manager.load_data(PM_FILE)
    shop_jobs_df = data_manager.load_data(SHOP_JOBS_FILE)

    stats = {
        'total_drivers': len(drivers_df),
        'cd_drivers': len(drivers_df[drivers_df['driver_type'] == 'CD']) if not drivers_df.empty else 0,
        'total_trucks': len(trucks_df),
        'active_trucks': len(trucks_df[trucks_df['status'] == 'Active']) if not trucks_df.empty else 0,
        'total_trailers': len(trailers_df),
        'available_trailers': len(trailers_df[trailers_df['status'] == 'Available']) if not trailers_df.empty else 0,
        'total_maintenance': len(maintenance_df),
        'open_otr': len(otr_df[otr_df['status'] == 'Open']) if not otr_df.empty else 0,
        'total_pm': len(pm_df),
        'shop_jobs': len(shop_jobs_df),
        'total_maintenance_cost': maintenance_df['total_cost'].sum() if not maintenance_df.empty else 0,
        'total_otr_cost': otr_df['total_cost'].sum() if not otr_df.empty else 0
    }

    return stats


# Routes
@app.route('/')
def dashboard():
    """Dashboard page"""
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


# Driver Routes
@app.route('/drivers')
def drivers():
    """Drivers management page"""
    drivers_df = data_manager.load_data(DRIVERS_FILE)
    drivers_list = drivers_df.to_dict('records') if not drivers_df.empty else []
    return render_template('drivers.html', drivers=drivers_list)


@app.route('/drivers/add', methods=['GET', 'POST'])
def add_driver():
    """Add new driver"""
    if request.method == 'POST':
        try:
            drivers_df = data_manager.load_data(DRIVERS_FILE)

            new_driver = {
                'driver_id': data_manager.generate_id(),
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'license_number': request.form['license_number'],
                'driver_type': request.form['driver_type'],
                'hire_date': request.form['hire_date'],
                'phone': request.form.get('phone', ''),
                'email': request.form.get('email', ''),
                'address': request.form.get('address', ''),
                'cdl_expiry': request.form.get('cdl_expiry', ''),
                'medical_expiry': request.form.get('medical_expiry', ''),
                'status': request.form['status'],
                'notes': request.form.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }

            drivers_df = pd.concat([drivers_df, pd.DataFrame([new_driver])], ignore_index=True)

            if data_manager.save_data(drivers_df, DRIVERS_FILE):
                flash('Driver added successfully!', 'success')
                return redirect(url_for('drivers'))
            else:
                flash('Error saving driver data!', 'error')

        except Exception as e:
            flash(f'Error adding driver: {str(e)}', 'error')

    return render_template('add_driver.html')


# Truck Routes
@app.route('/trucks')
def trucks():
    """Trucks management page"""
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trucks_list = trucks_df.to_dict('records') if not trucks_df.empty else []
    return render_template('trucks.html', trucks=trucks_list)


@app.route('/trucks/add', methods=['GET', 'POST'])
def add_truck():
    """Add new truck"""
    if request.method == 'POST':
        try:
            trucks_df = data_manager.load_data(TRUCKS_FILE)

            new_truck = {
                'truck_id': data_manager.generate_id(),
                'truck_number': request.form['truck_number'],
                'make': request.form['make'],
                'model': request.form['model'],
                'year': request.form['year'],
                'vin': request.form['vin'],
                'engine_type': request.form.get('engine_type', ''),
                'mileage': request.form.get('mileage', 0),
                'assigned_driver': request.form.get('assigned_driver', ''),
                'status': request.form['status'],
                'purchase_date': request.form.get('purchase_date', ''),
                'last_pm_date': request.form.get('last_pm_date', ''),
                'next_pm_due': request.form.get('next_pm_due', ''),
                'notes': request.form.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }

            trucks_df = pd.concat([trucks_df, pd.DataFrame([new_truck])], ignore_index=True)

            if data_manager.save_data(trucks_df, TRUCKS_FILE):
                flash('Truck added successfully!', 'success')
                return redirect(url_for('trucks'))
            else:
                flash('Error saving truck data!', 'error')

        except Exception as e:
            flash(f'Error adding truck: {str(e)}', 'error')

    # Load drivers for assignment dropdown
    drivers_df = data_manager.load_data(DRIVERS_FILE)
    drivers_list = drivers_df.to_dict('records') if not drivers_df.empty else []

    return render_template('add_truck.html', drivers=drivers_list)


# Trailer Routes
@app.route('/trailers')
def trailers():
    """Trailers management page"""
    trailers_df = data_manager.load_data(TRAILERS_FILE)
    trailers_list = trailers_df.to_dict('records') if not trailers_df.empty else []
    return render_template('trailers.html', trailers=trailers_list)


@app.route('/trailers/add', methods=['GET', 'POST'])
def add_trailer():
    """Add new trailer"""
    if request.method == 'POST':
        try:
            trailers_df = data_manager.load_data(TRAILERS_FILE)

            new_trailer = {
                'trailer_id': data_manager.generate_id(),
                'trailer_number': request.form['trailer_number'],
                'type': request.form['type'],
                'year': request.form['year'],
                'make': request.form['make'],
                'capacity': request.form.get('capacity', ''),
                'assigned_truck': request.form.get('assigned_truck', ''),
                'status': request.form['status'],
                'last_inspection': request.form.get('last_inspection', ''),
                'next_inspection_due': request.form.get('next_inspection_due', ''),
                'notes': request.form.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }

            trailers_df = pd.concat([trailers_df, pd.DataFrame([new_trailer])], ignore_index=True)

            if data_manager.save_data(trailers_df, TRAILERS_FILE):
                flash('Trailer added successfully!', 'success')
                return redirect(url_for('trailers'))
            else:
                flash('Error saving trailer data!', 'error')

        except Exception as e:
            flash(f'Error adding trailer: {str(e)}', 'error')

    # Load trucks for assignment dropdown
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trucks_list = trucks_df.to_dict('records') if not trucks_df.empty else []

    return render_template('add_trailer.html', trucks=trucks_list)


# OTR Repairs Routes
@app.route('/otr')
def otr_repairs():
    """OTR repairs management page"""
    otr_df = data_manager.load_data(OTR_FILE)
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    drivers_df = data_manager.load_data(DRIVERS_FILE)

    # Add truck and driver names to OTR records
    otr_list = []
    if not otr_df.empty:
        for _, row in otr_df.iterrows():
            otr_record = row.to_dict()

            # Add truck info
            if not trucks_df.empty:
                truck_info = trucks_df[trucks_df['truck_id'] == row['truck_id']]
                if not truck_info.empty:
                    otr_record['truck_number'] = truck_info.iloc[0]['truck_number']
                    otr_record['truck_make_model'] = f"{truck_info.iloc[0]['make']} {truck_info.iloc[0]['model']}"

            # Add driver info
            if not drivers_df.empty:
                driver_info = drivers_df[drivers_df['driver_id'] == row['driver_id']]
                if not driver_info.empty:
                    otr_record[
                        'driver_name'] = f"{driver_info.iloc[0]['first_name']} {driver_info.iloc[0]['last_name']}"

            otr_list.append(otr_record)

    return render_template('otr_repairs.html', otr_repairs=otr_list)


@app.route('/otr/add', methods=['GET', 'POST'])
def add_otr():
    """Add new OTR repair"""
    if request.method == 'POST':
        try:
            otr_df = data_manager.load_data(OTR_FILE)

            repair_cost = float(request.form.get('repair_cost', 0))
            tow_cost = float(request.form.get('tow_cost', 0))
            hotel_cost = float(request.form.get('hotel_cost', 0))
            total_cost = repair_cost + tow_cost + hotel_cost

            new_otr = {
                'otr_id': data_manager.generate_id(),
                'truck_id': request.form['truck_id'],
                'driver_id': request.form['driver_id'],
                'breakdown_date': request.form['breakdown_date'],
                'location': request.form['location'],
                'issue_description': request.form['issue_description'],
                'repair_shop': request.form['repair_shop'],
                'repair_cost': repair_cost,
                'parts_used': request.form.get('parts_used', ''),
                'labor_hours': float(request.form.get('labor_hours', 0)),
                'downtime_hours': float(request.form.get('downtime_hours', 0)),
                'tow_cost': tow_cost,
                'hotel_cost': hotel_cost,
                'total_cost': total_cost,
                'insurance_claim': 'insurance_claim' in request.form,
                'status': request.form['status'],
                'notes': request.form.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }

            otr_df = pd.concat([otr_df, pd.DataFrame([new_otr])], ignore_index=True)

            if data_manager.save_data(otr_df, OTR_FILE):
                flash('OTR repair added successfully!', 'success')
                return redirect(url_for('otr_repairs'))
            else:
                flash('Error saving OTR repair data!', 'error')

        except Exception as e:
            flash(f'Error adding OTR repair: {str(e)}', 'error')

    # Load trucks and drivers for dropdowns
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    drivers_df = data_manager.load_data(DRIVERS_FILE)
    trucks_list = trucks_df.to_dict('records') if not trucks_df.empty else []
    drivers_list = drivers_df.to_dict('records') if not drivers_df.empty else []

    return render_template('add_otr.html', trucks=trucks_list, drivers=drivers_list)


# PM Records Routes
@app.route('/pm')
def pm_records():
    """PM records management page"""
    pm_df = data_manager.load_data(PM_FILE)
    trucks_df = data_manager.load_data(TRUCKS_FILE)

    # Add truck info to PM records
    pm_list = []
    if not pm_df.empty:
        for _, row in pm_df.iterrows():
            pm_record = row.to_dict()

            # Add truck info
            if not trucks_df.empty:
                truck_info = trucks_df[trucks_df['truck_id'] == row['truck_id']]
                if not truck_info.empty:
                    pm_record['truck_number'] = truck_info.iloc[0]['truck_number']
                    pm_record['truck_make_model'] = f"{truck_info.iloc[0]['make']} {truck_info.iloc[0]['model']}"

            pm_list.append(pm_record)

    return render_template('pm_records.html', pm_records=pm_list)


@app.route('/pm/add', methods=['GET', 'POST'])
def add_pm():
    """Add new PM record"""
    if request.method == 'POST':
        try:
            pm_df = data_manager.load_data(PM_FILE)

            parts_cost = float(request.form.get('parts_cost', 0))
            labor_cost = float(request.form.get('labor_cost', 0))
            total_cost = parts_cost + labor_cost

            new_pm = {
                'pm_id': data_manager.generate_id(),
                'truck_id': request.form['truck_id'],
                'pm_type': request.form['pm_type'],
                'date': request.form['date'],
                'mileage': int(request.form.get('mileage', 0)),
                'next_due_date': request.form.get('next_due_date', ''),
                'next_due_mileage': int(request.form.get('next_due_mileage', 0)),
                'shop_name': request.form['shop_name'],
                'technician': request.form.get('technician', ''),
                'oil_change': 'oil_change' in request.form,
                'filter_change': 'filter_change' in request.form,
                'inspection_items': request.form.get('inspection_items', ''),
                'parts_cost': parts_cost,
                'labor_cost': labor_cost,
                'total_cost': total_cost,
                'status': request.form['status'],
                'notes': request.form.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }

            pm_df = pd.concat([pm_df, pd.DataFrame([new_pm])], ignore_index=True)

            if data_manager.save_data(pm_df, PM_FILE):
                flash('PM record added successfully!', 'success')
                return redirect(url_for('pm_records'))
            else:
                flash('Error saving PM record data!', 'error')

        except Exception as e:
            flash(f'Error adding PM record: {str(e)}', 'error')

    # Load trucks for dropdown
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trucks_list = trucks_df.to_dict('records') if not trucks_df.empty else []

    return render_template('add_pm.html', trucks=trucks_list)


# Shop Jobs Routes
@app.route('/shop_jobs')
def shop_jobs():
    """Shop jobs management page"""
    shop_jobs_df = data_manager.load_data(SHOP_JOBS_FILE)
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trailers_df = data_manager.load_data(TRAILERS_FILE)

    # Add truck and trailer info to shop jobs
    shop_jobs_list = []
    if not shop_jobs_df.empty:
        for _, row in shop_jobs_df.iterrows():
            job_record = row.to_dict()

            # Add truck info
            if row['truck_id'] and not trucks_df.empty:
                truck_info = trucks_df[trucks_df['truck_id'] == row['truck_id']]
                if not truck_info.empty:
                    job_record['truck_number'] = truck_info.iloc[0]['truck_number']

            # Add trailer info
            if row['trailer_id'] and not trailers_df.empty:
                trailer_info = trailers_df[trailers_df['trailer_id'] == row['trailer_id']]
                if not trailer_info.empty:
                    job_record['trailer_number'] = trailer_info.iloc[0]['trailer_number']

            shop_jobs_list.append(job_record)

    return render_template('shop_jobs.html', shop_jobs=shop_jobs_list)


@app.route('/shop_jobs/add', methods=['GET', 'POST'])
def add_shop_job():
    """Add new shop job"""
    if request.method == 'POST':
        try:
            shop_jobs_df = data_manager.load_data(SHOP_JOBS_FILE)

            parts_cost = float(request.form.get('parts_cost', 0))
            labor_cost = float(request.form.get('labor_cost', 0))
            total_cost = parts_cost + labor_cost

            new_shop_job = {
                'job_id': data_manager.generate_id(),
                'truck_id': request.form.get('truck_id', ''),
                'trailer_id': request.form.get('trailer_id', ''),
                'job_type': request.form['job_type'],
                'date_started': request.form['date_started'],
                'date_completed': request.form.get('date_completed', ''),
                'description': request.form['description'],
                'technician': request.form['technician'],
                'parts_used': request.form.get('parts_used', ''),
                'labor_hours': float(request.form.get('labor_hours', 0)),
                'parts_cost': parts_cost,
                'labor_cost': labor_cost,
                'total_cost': total_cost,
                'status': request.form['status'],
                'priority': request.form['priority'],
                'notes': request.form.get('notes', ''),
                'created_at': datetime.now().isoformat()
            }

            shop_jobs_df = pd.concat([shop_jobs_df, pd.DataFrame([new_shop_job])], ignore_index=True)

            if data_manager.save_data(shop_jobs_df, SHOP_JOBS_FILE):
                flash('Shop job added successfully!', 'success')
                return redirect(url_for('shop_jobs'))
            else:
                flash('Error saving shop job data!', 'error')

        except Exception as e:
            flash(f'Error adding shop job: {str(e)}', 'error')

    # Load trucks and trailers for dropdowns
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trailers_df = data_manager.load_data(TRAILERS_FILE)
    trucks_list = trucks_df.to_dict('records') if not trucks_df.empty else []
    trailers_list = trailers_df.to_dict('records') if not trailers_df.empty else []

    return render_template('add_shop_job.html', trucks=trucks_list, trailers=trailers_list)


# Search and Reports Routes
@app.route('/search')
def search():
    """Search page"""
    return render_template('search.html')


@app.route('/search/truck/<truck_id>')
def truck_report(truck_id):
    """Generate truck report"""
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    maintenance_df = data_manager.load_data(MAINTENANCE_FILE)
    otr_df = data_manager.load_data(OTR_FILE)
    pm_df = data_manager.load_data(PM_FILE)
    shop_jobs_df = data_manager.load_data(SHOP_JOBS_FILE)
    drivers_df = data_manager.load_data(DRIVERS_FILE)

    # Get truck info
    truck_info = trucks_df[trucks_df['truck_id'] == truck_id]
    if truck_info.empty:
        flash('Truck not found!', 'error')
        return redirect(url_for('search'))

    truck = truck_info.iloc[0].to_dict()

    # Get related records
    truck_maintenance = maintenance_df[maintenance_df['truck_id'] == truck_id].to_dict('records')
    truck_otr = otr_df[otr_df['truck_id'] == truck_id].to_dict('records')
    truck_pm = pm_df[pm_df['truck_id'] == truck_id].to_dict('records')
    truck_shop = shop_jobs_df[shop_jobs_df['truck_id'] == truck_id].to_dict('records')

    # Calculate totals
    total_maintenance_cost = sum(float(record.get('total_cost', 0)) for record in truck_maintenance)
    total_otr_cost = sum(float(record.get('total_cost', 0)) for record in truck_otr)
    total_pm_cost = sum(float(record.get('total_cost', 0)) for record in truck_pm)
    total_shop_cost = sum(float(record.get('total_cost', 0)) for record in truck_shop)

    totals = {
        'maintenance': total_maintenance_cost,
        'otr': total_otr_cost,
        'pm': total_pm_cost,
        'shop': total_shop_cost,
        'grand_total': total_maintenance_cost + total_otr_cost + total_pm_cost + total_shop_cost
    }

    return render_template('truck_report.html',
                           truck=truck,
                           maintenance=truck_maintenance,
                           otr_repairs=truck_otr,
                           pm_records=truck_pm,
                           shop_jobs=truck_shop,
                           totals=totals)


@app.route('/search/driver/<driver_id>')
def driver_report(driver_id):
    """Generate driver report"""
    drivers_df = data_manager.load_data(DRIVERS_FILE)
    otr_df = data_manager.load_data(OTR_FILE)
    trucks_df = data_manager.load_data(TRUCKS_FILE)

    # Get driver info
    driver_info = drivers_df[drivers_df['driver_id'] == driver_id]
    if driver_info.empty:
        flash('Driver not found!', 'error')
        return redirect(url_for('search'))

    driver = driver_info.iloc[0].to_dict()

    # Get assigned truck
    driver_name = f"{driver['first_name']} {driver['last_name']}"
    assigned_truck = trucks_df[trucks_df['assigned_driver'] == driver_name]
    truck = assigned_truck.iloc[0].to_dict() if not assigned_truck.empty else None

    # Get OTR records
    driver_otr = otr_df[otr_df['driver_id'] == driver_id].to_dict('records')

    # Calculate totals
    total_otr_cost = sum(float(record.get('total_cost', 0)) for record in driver_otr)
    total_downtime = sum(float(record.get('downtime_hours', 0)) for record in driver_otr)

    totals = {
        'otr_cases': len(driver_otr),
        'otr_cost': total_otr_cost,
        'downtime_hours': total_downtime
    }

    return render_template('driver_report.html',
                           driver=driver,
                           truck=truck,
                           otr_repairs=driver_otr,
                           totals=totals)


@app.route('/search/trailer/<trailer_id>')
def trailer_report(trailer_id):
    """Generate trailer report"""
    trailers_df = data_manager.load_data(TRAILERS_FILE)
    maintenance_df = data_manager.load_data(MAINTENANCE_FILE)
    shop_jobs_df = data_manager.load_data(SHOP_JOBS_FILE)

    # Get trailer info
    trailer_info = trailers_df[trailers_df['trailer_id'] == trailer_id]
    if trailer_info.empty:
        flash('Trailer not found!', 'error')
        return redirect(url_for('search'))

    trailer = trailer_info.iloc[0].to_dict()

    # Get related records
    trailer_maintenance = maintenance_df[maintenance_df['trailer_id'] == trailer_id].to_dict('records')
    trailer_shop = shop_jobs_df[shop_jobs_df['trailer_id'] == trailer_id].to_dict('records')

    # Calculate totals
    total_maintenance_cost = sum(float(record.get('total_cost', 0)) for record in trailer_maintenance)
    total_shop_cost = sum(float(record.get('total_cost', 0)) for record in trailer_shop)

    totals = {
        'maintenance': total_maintenance_cost,
        'shop': total_shop_cost,
        'total': total_maintenance_cost + total_shop_cost
    }

    return render_template('trailer_report.html',
                           trailer=trailer,
                           maintenance=trailer_maintenance,
                           shop_jobs=trailer_shop,
                           totals=totals)


# API Routes for AJAX calls
@app.route('/api/trucks')
def api_trucks():
    """API endpoint to get trucks list"""
    trucks_df = data_manager.load_data(TRUCKS_FILE)
    trucks_list = trucks_df.to_dict('records') if not trucks_df.empty else []
    return jsonify(trucks_list)


@app.route('/api/drivers')
def api_drivers():
    """API endpoint to get drivers list"""
    drivers_df = data_manager.load_data(DRIVERS_FILE)
    drivers_list = drivers_df.to_dict('records') if not drivers_df.empty else []
    return jsonify(drivers_list)


@app.route('/api/trailers')
def api_trailers():
    """API endpoint to get trailers list"""
    trailers_df = data_manager.load_data(TRAILERS_FILE)
    trailers_list = trailers_df.to_dict('records') if not trailers_df.empty else []
    return jsonify(trailers_list)


# Data Export/Import Routes
@app.route('/export')
def export_data():
    """Export all data to JSON"""
    try:
        all_data = {
            'drivers': data_manager.load_data(DRIVERS_FILE).to_dict('records'),
            'trucks': data_manager.load_data(TRUCKS_FILE).to_dict('records'),
            'trailers': data_manager.load_data(TRAILERS_FILE).to_dict('records'),
            'maintenance': data_manager.load_data(MAINTENANCE_FILE).to_dict('records'),
            'otr_repairs': data_manager.load_data(OTR_FILE).to_dict('records'),
            'pm_records': data_manager.load_data(PM_FILE).to_dict('records'),
            'shop_jobs': data_manager.load_data(SHOP_JOBS_FILE).to_dict('records'),
            'export_date': datetime.now().isoformat()
        }

        # Create backup file
        backup_filename = f"tms_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join(UPLOAD_FOLDER, backup_filename)

        with open(backup_path, 'w') as f:
            json.dump(all_data, f, indent=2, default=str)

        return send_file(backup_path, as_attachment=True, download_name=backup_filename)

    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/import', methods=['GET', 'POST'])
def import_data():
    """Import data from JSON backup"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                with open(filepath, 'r') as f:
                    import_data_dict = json.load(f)

                # Restore data
                if 'drivers' in import_data_dict:
                    pd.DataFrame(import_data_dict['drivers']).to_csv(DRIVERS_FILE, index=False)

                if 'trucks' in import_data_dict:
                    pd.DataFrame(import_data_dict['trucks']).to_csv(TRUCKS_FILE, index=False)

                if 'trailers' in import_data_dict:
                    pd.DataFrame(import_data_dict['trailers']).to_csv(TRAILERS_FILE, index=False)

                if 'maintenance' in import_data_dict:
                    pd.DataFrame(import_data_dict['maintenance']).to_csv(MAINTENANCE_FILE, index=False)

                if 'otr_repairs' in import_data_dict:
                    pd.DataFrame(import_data_dict['otr_repairs']).to_csv(OTR_FILE, index=False)

                if 'pm_records' in import_data_dict:
                    pd.DataFrame(import_data_dict['pm_records']).to_csv(PM_FILE, index=False)

                if 'shop_jobs' in import_data_dict:
                    pd.DataFrame(import_data_dict['shop_jobs']).to_csv(SHOP_JOBS_FILE, index=False)

                flash('Data imported successfully!', 'success')

                # Clean up uploaded file
                os.remove(filepath)

            except Exception as e:
                flash(f'Import failed: {str(e)}', 'error')

        else:
            flash('Invalid file type. Please upload a JSON file.', 'error')

    return render_template('import_data.html')


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)