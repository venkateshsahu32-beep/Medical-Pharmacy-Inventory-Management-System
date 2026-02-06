# Smart Pharmacy Inventory Management System

A comprehensive web application for pharmacy inventory management built with Flask, SQLAlchemy, and Bootstrap 5.

## 🎯 Project Overview

This system provides complete pharmacy inventory management with intelligent features including:
- Real-time inventory tracking
- Automated stock alerts
- Seasonal medicine recommendations
- Integrated billing system with automatic stock deduction
- Expiry date monitoring

## 📋 Features

### 1. **Dashboard**
- Total stock summary
- Today's sales tracking
- Critical alerts for:
  - Medicines expiring in < 30 days
  - Low stock items (< 10 units)
- Seasonal recommendations based on current month

### 2. **Inventory Management (CRUD)**
- Add new medicines
- Update existing medicine details
- Delete medicines
- Real-time search functionality
- Sortable data tables

### 3. **Smart Data Seeding**
- Automated generation of 1000+ medicine records
- CSV import capability
- Data cleaning and validation
- Automatic seasonal tagging

### 4. **Billing System**
- Medicine selection with stock validation
- Shopping cart functionality
- Invoice generation (print-ready)
- Automatic stock deduction
- Sales tracking

### 5. **Seasonal Recommendations**
- Intelligent medicine categorization
- Season-based stocking suggestions
- Current: Winter season (February)

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0
- **JavaScript**: Vanilla JS for dynamic interactions
- **Data Processing**: Pandas 2.1.4

## 📁 Project Structure

```
pharmacy-management/
├── app.py                    # Main Flask application
├── models.py                 # SQLAlchemy database models
├── seed_data.py             # Data seeding script
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── pharmacy.db              # SQLite database
├── medicines_dataset.csv    # Sample dataset
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── main.js         # JavaScript utilities
└── templates/
    ├── base.html           # Base template
    ├── dashboard.html      # Dashboard page
    ├── inventory.html      # Inventory management
    ├── add_medicine.html   # Add medicine form
    ├── edit_medicine.html  # Edit medicine form
    ├── billing.html        # Billing system
    └── invoice.html        # Invoice template
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Seed the Database
```bash
python seed_data.py
```

This will:
- Create the SQLite database
- Generate 1000+ medicine records
- Add 5 supplier records
- Display statistics

### Step 3: Run the Application
```bash
python app.py
```

The application will be available at: **https://medical-pharmacy-inventory-manageme.vercel.app/**

## 📊 Database Schema

### Medicine Table
- `id`: Primary key
- `name`: Medicine name
- `manufacturer`: Manufacturer name
- `category`: Medicine category
- `price`: Unit price
- `stock_quantity`: Current stock
- `expiry_date`: Expiry date
- `seasonal_tag`: Season (Winter/Summer/Monsoon/Spring)
- `created_at`, `updated_at`: Timestamps

### Sales Table
- `id`: Primary key
- `medicine_id`: Foreign key to Medicine
- `quantity_sold`: Quantity sold
- `total_amount`: Total sale amount
- `sale_date`: Sale timestamp

### Supplier Table
- `id`: Primary key
- `name`: Supplier name
- `contact`: Phone number
- `email`: Email address
- `address`: Physical address

## 🎨 Features Demonstration

### Dashboard Statistics (After Seeding)
- **Total Stock**: 1000 medicines
- **Low Stock Items**: 52 items
- **Expiring Soon**: 196 medicines
- **Current Season**: Winter (February 2026)

### Seasonal Logic
The system automatically tags medicines by season:
- **Winter**: Cough Syrup, Cold Relief, Throat Lozenges, Decongestant, Vitamin C
- **Monsoon**: Antifungal, Antibiotic, Antiseptic, Anti-diarrheal
- **Summer**: Antacid, Oral Rehydration, Antihistamine
- **Spring**: Antihistamine, Allergy Relief, Eye Drops, Nasal Spray

## 🔍 Usage Guide

### Adding a Medicine
1. Navigate to **Inventory** → **Add New Medicine**
2. Fill in the form:
   - Medicine Name (e.g., "Paracetamol 500mg")
   - Manufacturer
   - Category (dropdown)
   - Price
   - Stock Quantity
   - Expiry Date
3. Click **Add Medicine**

### Searching Inventory
1. Go to **Inventory** page
2. Use the search bar to filter by:
   - Medicine name
   - Manufacturer
   - Category
3. Results update in real-time

### Creating a Bill
1. Navigate to **Billing**
2. Select medicine from dropdown
3. Enter quantity (validates against stock)
4. Click **Add** to add to cart
5. Repeat for multiple items
6. Click **Generate Invoice**
7. Invoice opens in new view (print-ready)
8. Stock is automatically deducted

### Monitoring Alerts
1. Dashboard shows two critical alert tables:
   - **Expiring Soon**: Medicines with < 30 days until expiry
   - **Low Stock**: Medicines with < 10 units
2. Click **Restock** button to edit and update stock

## 🎓 For Viva Presentation

### Key Points to Highlight:

1. **Modular Code Structure**: Separate files for models, routes, and configuration
2. **ORM Usage**: SQLAlchemy for database operations (no raw SQL)
3. **Data Validation**: Form validation and stock checking
4. **Business Logic**: Helper methods in models (is_expiring_soon, is_low_stock)
5. **Responsive Design**: Bootstrap 5 for mobile-friendly interface
6. **Real-time Features**: JavaScript for search and cart management
7. **Seasonal Intelligence**: Automatic categorization based on medicine type
8. **Scalability**: Can handle 1000+ records efficiently

### Code Comments
All files include detailed comments explaining:
- Purpose of each function
- Business logic decisions
- Database relationships
- Frontend interactions

## 📝 API Endpoints

- `GET /` - Dashboard
- `GET /inventory` - View all medicines
- `GET /inventory/add` - Add medicine form
- `POST /inventory/add` - Create medicine
- `GET /inventory/edit/<id>` - Edit medicine form
- `POST /inventory/edit/<id>` - Update medicine
- `POST /inventory/delete/<id>` - Delete medicine
- `GET /billing` - Billing page
- `POST /generate_invoice` - Process sale and generate invoice
- `GET /api/seasonal_recommendations` - Get seasonal medicines (JSON)
- `GET /api/medicine/<id>` - Get medicine details (JSON)

## 🔐 Security Notes

- CSRF protection via Flask secret key
- Input validation on all forms
- SQL injection prevention via ORM
- Stock validation before sales

## 📈 Future Enhancements

- User authentication and roles
- Supplier management integration
- Advanced reporting and analytics
- Email alerts for expiring medicines
- Barcode scanning support
- Multi-pharmacy support

## 👨‍💻 Developer

**Senior Full Stack Python Developer**
- Academic Project for Pharmacy Management
- Built with Flask, SQLAlchemy, Bootstrap 5
- February 2026

## 📄 License

This is an academic project for educational purposes.

---

**Access the application**: https://medical-pharmacy-inventory-manageme.vercel.app/

**Database**: pharmacy.db (SQLite)

**Total Records**: 1000+ medicines, 5 suppliers


