import json
import random
from datetime import datetime, timedelta
import names  # Assuming names library for random names; if not, use alternatives

# Sample data (pasted from the user's JSON)
sample_data = {
  "export_date": "2025-01-15T10:30:00Z",
  "data_version": "TMS v1.0",
  "drivers": [ ... ],  # Omitted for brevity, but include the full sample JSON here in actual code
  # ... (full JSON)
}

# In actual execution, paste the full JSON as a string and load it
# For this, assume it's loaded as sample_data

# Function to generate random date between two dates
def random_date(start, end):
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime('%Y-%m-%d')

# Lists for randomization
first_names = ['John', 'Sarah', 'Michael', 'Lisa', 'Robert', 'Emily', 'David', 'Jennifer', 'James', 'Mary']
last_names = ['Martinez', 'Johnson', 'Thompson', 'Rodriguez', 'Wilson', 'Smith', 'Brown', 'Davis', 'Miller', 'Anderson']
makes = ['Freightliner', 'Peterbilt', 'Kenworth', 'Volvo']
models = ['Cascadia', '579', 'T680', 'VNL 760']
engine_types = ['DD15', 'PACCAR MX-13', 'PACCAR MX-11', 'D13', 'DD13']
trailer_types = ['Dry Van', 'Refrigerated', 'Flatbed']
trailer_makes = ['Great Dane', 'Utility', 'Fontaine', 'Wabash']
cities = ['Dallas, TX', 'Houston, TX', 'Austin, TX', 'San Antonio, TX', 'Fort Worth, TX', 'Oklahoma', 'Louisiana', 'Denver, CO']
statuses = ['Active', 'Maintenance', 'Available', 'Assigned']
maintenance_types = ['Routine Maintenance', 'Brake Service', 'Inspection']
otr_issues = ['Alternator failure', 'Tire blowout', 'DEF system malfunction']
pm_types = ['A Service', 'B Service', 'C Service']
shop_job_types = ['Engine Work', 'Brake Work', 'Routine Service']
technicians = ['Mike Stevens', 'Pete Williams', 'Tom Garcia', 'Jim Anderson', 'Ken Miller', 'Dave Richardson', 'Carlos Lopez']

# Generate 400 drivers
drivers = []
for i in range(1, 401):
    d = random.choice(sample_data['drivers'])  # Base on sample
    driver_id = f"d{i:03d}"
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    drivers.append({
        "driver_id": driver_id,
        "first_name": first_name,
        "last_name": last_name,
        "license_number": f"CDL{random.randint(100000,999999)}",
        "driver_type": random.choice(['CD', 'LP', 'LP Owner']),
        "hire_date": random_date(datetime(2019,1,1), datetime(2024,12,31)),
        "phone": f"555-0{random.randint(100,999)}",
        "email": f"{first_name[0].lower()}.{last_name.lower()}@company.com",
        "address": f"{random.randint(1000,9999)} {random.choice(['Main St', 'Oak Ave', 'Pine St'])}, {random.choice(cities)}",
        "cdl_expiry": random_date(datetime(2025,1,1), datetime(2027,12,31)),
        "medical_expiry": random_date(datetime(2025,1,1), datetime(2026,12,31)),
        "status": random.choice(statuses),
        "notes": random.choice(["Experienced driver", "New hire", "Senior driver"]),
        "created_at": datetime.now().isoformat() + 'Z'
    })

# Generate 400 trucks, assign random driver
trucks = []
driver_ids = [d['driver_id'] for d in drivers]
for i in range(1, 401):
    t = random.choice(sample_data['trucks'])
    truck_id = f"t{i:03d}"
    assigned_driver_id = random.choice(driver_ids)
    trucks.append({
        "truck_id": truck_id,
        "truck_number": f"T8{i:03d}",
        "make": random.choice(makes),
        "model": random.choice(models),
        "year": str(random.randint(2019,2024)),
        "vin": f"1{random.choice(['FUJGLDR', 'XPBDP9X', 'XKYDP9X', 'V4NC9EH'])}{random.randint(1000000,9999999)}",
        "engine_type": random.choice(engine_types),
        "mileage": str(random.randint(50000, 400000)),
        "assigned_driver": assigned_driver_id,  # Use ID instead of name for connection
        "status": random.choice(statuses),
        "purchase_date": random_date(datetime(2019,1,1), datetime(2024,12,31)),
        "last_pm_date": random_date(datetime(2024,1,1), datetime(2024,12,31)),
        "next_pm_due": random_date(datetime(2025,1,1), datetime(2025,12,31)),
        "notes": random.choice(["High mileage", "Lease unit", "New unit"]),
        "created_at": datetime.now().isoformat() + 'Z'
    })

# Generate 400 trailers, assign random truck
trailers = []
truck_ids = [t['truck_id'] for t in trucks]
for i in range(1, 401):
    tr = random.choice(sample_data['trailers'])
    trailer_id = f"tr{i:03d}"
    assigned_truck_id = random.choice(truck_ids + [''])  # Sometimes empty
    trailers.append({
        "trailer_id": trailer_id,
        "trailer_number": f"TR5{i:03d}",
        "type": random.choice(trailer_types),
        "year": str(random.randint(2019,2024)),
        "make": random.choice(trailer_makes),
        "capacity": random.choice(["53' - 110,000 lbs", "48' - 80,000 lbs", "53' - 105,000 lbs"]),
        "assigned_truck": assigned_truck_id,
        "status": random.choice(statuses),
        "last_inspection": random_date(datetime(2024,1,1), datetime(2024,12,31)),
        "next_inspection_due": random_date(datetime(2025,1,1), datetime(2025,12,31)),
        "notes": random.choice(["Good condition", "New trailer", "In maintenance"]),
        "created_at": datetime.now().isoformat() + 'Z'
    })

# Generate 400 maintenance records
maintenance = []
for i in range(1, 401):
    m = random.choice(sample_data['maintenance'])
    maintenance_id = f"m{i:03d}"
    truck_id = random.choice(truck_ids + [''])
    trailer_id = random.choice(trailer_ids + ['']) if truck_id == '' else ''
    maintenance.append({
        "maintenance_id": maintenance_id,
        "truck_id": truck_id,
        "trailer_id": trailer_id,
        "maintenance_type": random.choice(maintenance_types),
        "date": random_date(datetime(2024,1,1), datetime(2024,12,31)),
        "mileage": str(random.randint(0, 400000)) if truck_id else "0",
        "description": "Random maintenance description",
        "parts_cost": f"{random.uniform(50,500):.2f}",
        "labor_cost": f"{random.uniform(100,300):.2f}",
        "total_cost": f"{random.uniform(150,800):.2f}",
        "shop_name": random.choice(["Company Shop", "Pete's Service", "Cold Chain"]),
        "shop_location": random.choice(cities),
        "technician": random.choice(technicians),
        "status": "Completed",
        "notes": "Random note",
        "created_at": datetime.now().isoformat() + 'Z'
    })

# Similarly for otr_repairs (400)
otr_repairs = []
for i in range(1, 401):
    o = random.choice(sample_data['otr_repairs'])
    otr_id = f"otr{i:03d}"
    truck_id = random.choice(truck_ids)
    driver_id = random.choice(driver_ids)
    otr_repairs.append({
        "otr_id": otr_id,
        "truck_id": truck_id,
        "driver_id": driver_id,
        "breakdown_date": random_date(datetime(2024,1,1), datetime(2024,12,31)),
        "location": random.choice(["I-35 MM {random.randint(100,300)}", "Truck Stop - {random.choice(cities)}"]),
        "issue_description": random.choice(otr_issues),
        "repair_shop": "Random Repair Shop",
        "repair_cost": f"{random.uniform(200,1000):.2f}",
        "parts_used": "Random parts",
        "labor_hours": f"{random.uniform(1,10):.1f}",
        "downtime_hours": f"{random.uniform(2,24):.1f}",
        "tow_cost": f"{random.uniform(0,500):.2f}",
        "hotel_cost": f"{random.uniform(0,200):.2f}",
        "total_cost": f"{random.uniform(200,1500):.2f}",
        "insurance_claim": random.choice([True, False]),
        "status": "Completed",
        "notes": "Random OTR note",
        "created_at": datetime.now().isoformat() + 'Z'
    })

# PM records (400)
pm_records = []
for i in range(1, 401):
    p = random.choice(sample_data['pm_records'])
    pm_id = f"pm{i:03d}"
    truck_id = random.choice(truck_ids)
    pm_records.append({
        "pm_id": pm_id,
        "truck_id": truck_id,
        "pm_type": random.choice(pm_types),
        "date": random_date(datetime(2024,1,1), datetime(2024,12,31)),
        "mileage": str(random.randint(50000, 400000)),
        "next_due_date": random_date(datetime(2025,1,1), datetime(2025,12,31)),
        "next_due_mileage": str(random.randint(100000, 500000)),
        "shop_name": "Random Shop",
        "technician": random.choice(technicians),
        "oil_change": random.choice([True, False]),
        "filter_change": random.choice([True, False]),
        "inspection_items": "Random items",
        "parts_cost": f"{random.uniform(100,700):.2f}",
        "labor_cost": f"{random.uniform(100,500):.2f}",
        "total_cost": f"{random.uniform(200,1200):.2f}",
        "status": "Completed",
        "notes": "Random PM note",
        "created_at": datetime.now().isoformat() + 'Z'
    })

# Shop jobs (400)
shop_jobs = []
for i in range(1, 401):
    s = random.choice(sample_data['shop_jobs'])
    job_id = f"sj{i:03d}"
    truck_id = random.choice(truck_ids + [''])
    trailer_id = random.choice(trailer_ids + ['']) if truck_id == '' else ''
    date_started = random_date(datetime(2024,1,1), datetime(2024,12,31))
    date_completed = (datetime.strptime(date_started, '%Y-%m-%d') + timedelta(days=random.randint(1,10))).strftime('%Y-%m-%d')
    shop_jobs.append({
        "job_id": job_id,
        "truck_id": truck_id,
        "trailer_id": trailer_id,
        "job_type": random.choice(shop_job_types),
        "date_started": date_started,
        "date_completed": date_completed,
        "description": "Random job description",
        "technician": random.choice(technicians),
        "parts_used": "Random parts used",
        "labor_hours": f"{random.uniform(2,40):.1f}",
        "parts_cost": f"{random.uniform(200,4000):.2f}",
        "labor_cost": f"{random.uniform(100,2000):.2f}",
        "total_cost": f"{random.uniform(300,6000):.2f}",
        "status": "Completed",
        "priority": random.choice(["High", "Medium", "Low"]),
        "notes": "Random shop note",
        "created_at": datetime.now().isoformat() + 'Z'
    })

# Compile full data
full_data = {
    "export_date": datetime.now().isoformat() + 'Z',
    "data_version": "TMS v1.0 Generated",
    "drivers": drivers,
    "trucks": trucks,
    "trailers": trailers,
    "maintenance": maintenance,
    "otr_repairs": otr_repairs,
    "pm_records": pm_records,
    "shop_jobs": shop_jobs
}

# Save to JSON file
with open('generated_tms_data.json', 'w') as f:
    json.dump(full_data, f, indent=2)

print("Generated 400 records for each type and saved to generated_tms_data.json")