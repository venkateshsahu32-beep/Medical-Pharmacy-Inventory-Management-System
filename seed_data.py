"""
Smart Data Seeding Script for Pharmacy Inventory Management System
Author: Senior Full Stack Python Developer
Purpose: Reads CSV file and populates database with 1000+ medicine records
Features: Data cleaning, validation, seasonal tagging, and bulk insertion
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from models import db, Medicine, Supplier
from config import Config
import os

# Medicine categories with seasonal tags
MEDICINE_DATA = {
    'Painkiller': ['Paracetamol', 'Ibuprofen', 'Aspirin', 'Diclofenac', 'Naproxen', 'Dolo', 'Crocin', 'Combiflam', 'Brufen', 'Disprin'],
    'Antibiotic': ['Amoxicillin', 'Azithromycin', 'Ciprofloxacin', 'Cephalexin', 'Doxycycline', 'Augmentin', 'Zithromax', 'Erythromycin', 'Clindamycin', 'Metronidazole'],
    'Antihistamine': ['Cetirizine', 'Loratadine', 'Fexofenadine', 'Diphenhydramine', 'Allegra', 'Zyrtec', 'Benadryl', 'Claritin', 'Chlorpheniramine', 'Promethazine'],
    'Antacid': ['Omeprazole', 'Ranitidine', 'Pantoprazole', 'Esomeprazole', 'Gelusil', 'Eno', 'Digene', 'Gaviscon', 'Rabeprazole', 'Lansoprazole'],
    'Cough Syrup': ['Benadryl Cough', 'Ascoril', 'Chericof', 'Corex', 'Glycodin', 'Phensedyl', 'Torex', 'Zedex', 'Grilinctus', 'Cofsils'],
    'Cold Relief': ['Sinarest', 'Vicks Action', 'D-Cold', 'Coldact', 'Wikoryl', 'Cheston', 'Febrex', 'Okacet Cold', 'Cetrizet Plus', 'Montair LC'],
    'Vitamin C': ['Limcee', 'Celin', 'Redoxon', 'Vitamin C Tablets', 'Ascorbic Acid', 'C-Vit', 'Cecon', 'Cebion', 'Citravite', 'Healthvit C'],
    'Antifungal': ['Fluconazole', 'Clotrimazole', 'Terbinafine', 'Ketoconazole', 'Candid', 'Canesten', 'Lamisil', 'Nizoral', 'Myconaz', 'Fungitop'],
    'Antiseptic': ['Dettol', 'Savlon', 'Betadine', 'Soframycin', 'Neosporin', 'Boroline', 'Burnol', 'Povidone Iodine', 'Hydrogen Peroxide', 'Spirit'],
    'Anti-diarrheal': ['Loperamide', 'Imodium', 'Eldoper', 'Lopamide', 'Pepto-Bismol', 'Econorm', 'Darolac', 'Bifilac', 'Sporlac', 'Vibact'],
    'Decongestant': ['Pseudoephedrine', 'Otrivin', 'Nasivion', 'Xylometazoline', 'Oxymetazoline', 'Nasoclear', 'Nasal Drops', 'Sinex', 'Afrin', 'Sudafed'],
    'Diabetes': ['Metformin', 'Glimepiride', 'Glibenclamide', 'Insulin', 'Januvia', 'Amaryl', 'Gluconorm', 'Glycomet', 'Diamicron', 'Galvus'],
    'Blood Thinner': ['Aspirin', 'Warfarin', 'Clopidogrel', 'Ecosprin', 'Plavix', 'Disprin CV', 'Deplatt', 'Clopilet', 'Loprin', 'Cardivas'],
    'Oral Rehydration': ['ORS', 'Electral', 'Pedialyte', 'Enerzal', 'Prolyte', 'Rehydrate', 'Hydralyte', 'Gatorade', 'Powerade', 'Glucon-D'],
    'Allergy Relief': ['Montair', 'Montelukast', 'Allegra M', 'Levocet', 'Rupanex', 'Telekast', 'Montina', 'Airlukast', 'Montek', 'Singulair'],
    'Eye Drops': ['Refresh Tears', 'Moisol', 'Systane', 'Gentamicin', 'Tobramycin', 'Ciplox', 'Vigamox', 'Moxiflox', 'Occuflox', 'Floxip'],
    'Nasal Spray': ['Flixonase', 'Nasocort', 'Nasonex', 'Fluticasone', 'Mometasone', 'Rhinocort', 'Beconase', 'Avamys', 'Dymista', 'Omnaris'],
    'Throat Lozenges': ['Strepsils', 'Vicks', 'Halls', 'Cofsils', 'Koflet', 'Honitus', 'Cepacol', 'Chloraseptic', 'Ricola', 'Fisherman Friend']
}

MANUFACTURERS = [
    'Cipla', 'Sun Pharma', 'Dr Reddy\'s', 'Lupin', 'Alkem', 'Torrent', 'Glenmark',
    'Zydus Cadila', 'Mankind', 'Micro Labs', 'GSK', 'Sanofi', 'Abbott', 'Pfizer',
    'Novartis', 'Bayer', 'Dabur', 'Himalaya', 'HealthKart', 'P&G', 'Centaur'
]

def assign_seasonal_tag(category):
    """
    Assigns seasonal tag based on medicine category
    Uses the seasonal mapping from config
    """
    for season, categories in Config.SEASONAL_CATEGORIES.items():
        if category in categories:
            return season
    return None  # No specific season

def generate_random_expiry_date():
    """
    Generates random expiry date
    70% future dates (6 months to 2 years)
    20% near expiry (1-30 days)
    10% recently expired
    """
    rand = random.random()
    today = datetime.now().date()
    
    if rand < 0.70:  # Future dates
        days_ahead = random.randint(180, 730)  # 6 months to 2 years
        return today + timedelta(days=days_ahead)
    elif rand < 0.90:  # Near expiry (for testing alerts)
        days_ahead = random.randint(1, 30)
        return today + timedelta(days=days_ahead)
    else:  # Recently expired (for testing)
        days_behind = random.randint(1, 60)
        return today - timedelta(days=days_behind)

def generate_medicines(count=1000):
    """
    Generates specified number of medicine records
    Returns a list of dictionaries
    """
    medicines = []
    
    for i in range(count):
        # Randomly select category and medicine name
        category = random.choice(list(MEDICINE_DATA.keys()))
        base_name = random.choice(MEDICINE_DATA[category])
        
        # Add variations (dosage, form)
        dosages = ['50mg', '100mg', '250mg', '500mg', '1000mg', '10ml', '100ml', '200ml']
        forms = ['Tablet', 'Capsule', 'Syrup', 'Suspension', 'Drops', 'Cream', 'Ointment']
        
        # 60% with dosage, 30% with form, 10% plain
        rand = random.random()
        if rand < 0.60:
            name = f"{base_name} {random.choice(dosages)}"
        elif rand < 0.90:
            name = f"{base_name} {random.choice(forms)}"
        else:
            name = base_name
        
        # Generate other fields
        manufacturer = random.choice(MANUFACTURERS)
        price = round(random.uniform(10.0, 500.0), 2)
        stock_quantity = random.randint(0, 200)  # Some will be low stock
        expiry_date = generate_random_expiry_date()
        seasonal_tag = assign_seasonal_tag(category)
        
        medicines.append({
            'name': name,
            'manufacturer': manufacturer,
            'category': category,
            'price': price,
            'stock_quantity': stock_quantity,
            'expiry_date': expiry_date,
            'seasonal_tag': seasonal_tag
        })
    
    return medicines

def seed_from_csv(app, csv_path):
    """
    Reads CSV file and seeds database
    Handles data cleaning and validation
    """
    print("\n" + "="*60)
    print("SMART PHARMACY SEEDING SCRIPT")
    print("="*60)
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"⚠ CSV file not found at: {csv_path}")
        print("📝 Generating sample dataset...")
        
        # Generate medicines programmatically
        medicines_data = generate_medicines(1000)
        
        # Create DataFrame
        df = pd.DataFrame(medicines_data)
        
        # Save to CSV for reference
        df.to_csv(csv_path, index=False)
        print(f"✓ Generated CSV with {len(df)} records")
    else:
        print(f"📂 Reading CSV from: {csv_path}")
        
        try:
            # Read CSV with pandas
            df = pd.read_csv(csv_path)
            print(f"✓ Loaded {len(df)} records from CSV")
            
            # Data cleaning
            print("\n🧹 Cleaning data...")
            
            # Remove duplicates
            original_count = len(df)
            df = df.drop_duplicates(subset=['name', 'manufacturer'], keep='first')
            if len(df) < original_count:
                print(f"  - Removed {original_count - len(df)} duplicate records")
            
            # Handle missing values
            df['manufacturer'].fillna('Unknown', inplace=True)
            df['category'].fillna('General', inplace=True)
            df['price'].fillna(df['price'].median(), inplace=True)
            
            # Assign random expiry dates if missing
            if 'expiry_date' in df.columns:
                df['expiry_date'] = pd.to_datetime(df['expiry_date'], errors='coerce')
                missing_dates = df['expiry_date'].isna().sum()
                if missing_dates > 0:
                    print(f"  - Assigning random expiry dates to {missing_dates} records")
                    df.loc[df['expiry_date'].isna(), 'expiry_date'] = [
                        generate_random_expiry_date() for _ in range(missing_dates)
                    ]
            else:
                print("  - No expiry_date column found, generating random dates")
                df['expiry_date'] = [generate_random_expiry_date() for _ in range(len(df))]
            
            # Add stock quantity if missing
            if 'stock_quantity' not in df.columns:
                df['stock_quantity'] = [random.randint(0, 200) for _ in range(len(df))]
            
            # Assign seasonal tags
            df['seasonal_tag'] = df['category'].apply(assign_seasonal_tag)
            
            print("✓ Data cleaning complete")
            
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            print("📝 Generating sample dataset instead...")
            medicines_data = generate_medicines(1000)
            df = pd.DataFrame(medicines_data)
    
    # Insert into database
    print(f"\n💾 Inserting {len(df)} records into database...")
    
    with app.app_context():
        try:
            # Clear existing data (optional - comment out to preserve existing data)
            Medicine.query.delete()
            db.session.commit()
            print("  - Cleared existing medicine records")
            
            # Bulk insert
            inserted_count = 0
            for _, row in df.iterrows():
                medicine = Medicine(
                    name=row['name'],
                    manufacturer=row['manufacturer'],
                    category=row['category'],
                    price=float(row['price']),
                    stock_quantity=int(row.get('stock_quantity', random.randint(0, 200))),
                    expiry_date=row['expiry_date'] if isinstance(row['expiry_date'], datetime) else pd.to_datetime(row['expiry_date']).date(),
                    seasonal_tag=row.get('seasonal_tag')
                )
                db.session.add(medicine)
                inserted_count += 1
                
                # Commit in batches of 100 for performance
                if inserted_count % 100 == 0:
                    db.session.commit()
                    print(f"  - Inserted {inserted_count} records...")
            
            # Final commit
            db.session.commit()
            print(f"\n✓ Successfully inserted {inserted_count} medicine records!")
            
            # Statistics
            print("\n" + "="*60)
            print("DATABASE STATISTICS")
            print("="*60)
            print(f"Total Medicines: {Medicine.query.count()}")
            print(f"Low Stock Items: {Medicine.query.filter(Medicine.stock_quantity < 10).count()}")
            print(f"Expiring Soon: {len([m for m in Medicine.query.all() if m.is_expiring_soon()])}")
            print("="*60 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error inserting data: {e}")
            raise

def seed_suppliers(app):
    """
    Seeds sample supplier data
    """
    print("📦 Seeding supplier data...")
    
    sample_suppliers = [
        {'name': 'MedSupply Co.', 'contact': '9876543210', 'email': 'contact@medsupply.com', 'address': 'Mumbai, Maharashtra'},
        {'name': 'PharmaDirect Ltd.', 'contact': '9876543211', 'email': 'info@pharmadirect.com', 'address': 'Delhi, NCR'},
        {'name': 'HealthCare Distributors', 'contact': '9876543212', 'email': 'sales@healthcare.com', 'address': 'Bangalore, Karnataka'},
        {'name': 'Wellness Suppliers', 'contact': '9876543213', 'email': 'support@wellness.com', 'address': 'Pune, Maharashtra'},
        {'name': 'MediQuick Traders', 'contact': '9876543214', 'email': 'orders@mediquick.com', 'address': 'Chennai, Tamil Nadu'}
    ]
    
    with app.app_context():
        try:
            Supplier.query.delete()
            for supplier_data in sample_suppliers:
                supplier = Supplier(**supplier_data)
                db.session.add(supplier)
            db.session.commit()
            print(f"✓ Inserted {len(sample_suppliers)} suppliers\n")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error inserting suppliers: {e}")

# Main execution
if __name__ == '__main__':
    from flask import Flask
    from config import Config
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("[OK] Database tables created")
    
    # Seed data
    seed_from_csv(app, Config.CSV_DATASET_PATH)
    seed_suppliers(app)
    
    print("🎉 Seeding complete! Your pharmacy database is ready.")
