# Quick Start Guide - Smart Pharmacy System

## 🚀 Running the Application

### Current Status
✅ Application is **RUNNING** on http://localhost:5000

### If You Need to Restart

```bash
# Navigate to project directory
cd c:\Users\venka\.gemini\antigravity\playground\velvet-lagoon

# Run the application
python app.py
```

## 📱 Access Points

- **Dashboard**: http://localhost:5000
- **Inventory**: http://localhost:5000/inventory
- **Billing**: http://localhost:5000/billing

## 🎯 Quick Test Workflow

### 1. View Dashboard
- Open http://localhost:5000
- See 4 summary cards
- Check alert tables (196 expiring, 52 low stock)
- View seasonal recommendations

### 2. Test Inventory
- Click "Inventory" in navigation
- Use search bar to find medicines
- Click "Add New Medicine" to add a test medicine
- Click edit icon to modify existing medicine
- Click delete icon to remove a medicine

### 3. Test Billing
- Click "Billing" in navigation
- Select a medicine from dropdown
- Enter quantity (validates against stock)
- Click "Add" to add to cart
- Repeat for multiple items
- Click "Generate Invoice"
- Invoice opens in new view
- Click "Print Invoice" to print
- Check inventory - stock should be deducted

## 📊 Database Info

- **Location**: `pharmacy.db`
- **Total Medicines**: 1000
- **Low Stock**: 52 items
- **Expiring Soon**: 196 items
- **Suppliers**: 5

## 🔄 Reset Database

If you want to reset the database:

```bash
# Delete the database
del pharmacy.db

# Re-seed
python seed_data.py
```

## 🎓 For Viva Demonstration

### Key Features to Show

1. **Dashboard Alerts**
   - Point out the two alert tables
   - Explain color coding (red/yellow badges)
   - Show seasonal recommendations

2. **Search Functionality**
   - Type in search bar
   - Show real-time filtering
   - Explain server-side vs client-side search

3. **CRUD Operations**
   - Add a new medicine
   - Edit an existing one
   - Show delete confirmation

4. **Billing System**
   - Add multiple items to cart
   - Show stock validation
   - Generate invoice
   - Demonstrate automatic stock deduction

5. **Code Walkthrough**
   - Show models.py (ORM, relationships)
   - Show app.py (routes, business logic)
   - Show seed_data.py (data generation)
   - Point out comments explaining logic

### Questions You Might Be Asked

**Q: How does seasonal recommendation work?**
A: The system maps medicine categories to seasons in config.py. During seeding, each medicine gets a seasonal tag. The dashboard queries medicines matching the current season (Winter for February).

**Q: How do you prevent overselling?**
A: In the billing route, before processing a sale, we check if requested quantity <= available stock. If not, we return an error and don't process the sale.

**Q: Why use SQLAlchemy instead of raw SQL?**
A: SQLAlchemy provides ORM benefits - automatic SQL generation, relationship management, migration support, and SQL injection prevention.

**Q: How does the expiry alert work?**
A: The Medicine model has a helper method `is_expiring_soon()` that calculates days until expiry and returns True if < 30 days.

## 📝 File Locations

- **Main App**: `app.py`
- **Models**: `models.py`
- **Seeding**: `seed_data.py`
- **Config**: `config.py`
- **Templates**: `templates/` folder
- **Static Files**: `static/` folder
- **Database**: `pharmacy.db`
- **Documentation**: `README.md`

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Database Locked
```bash
# Close all connections and restart
del pharmacy.db
python seed_data.py
python app.py
```

### Dependencies Missing
```bash
pip install -r requirements.txt
```

## ✅ Checklist Before Viva

- [ ] Application running on http://localhost:5000
- [ ] Database has 1000 medicines
- [ ] All pages accessible (Dashboard, Inventory, Billing)
- [ ] Can add/edit/delete medicines
- [ ] Can generate invoice
- [ ] Understand seasonal logic
- [ ] Can explain ORM benefits
- [ ] Know location of all files

---

**Current Status**: ✅ All systems operational

**Application**: http://localhost:5000

**Ready for**: Demonstration & Viva Presentation
