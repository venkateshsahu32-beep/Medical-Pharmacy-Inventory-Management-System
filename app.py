"""
Smart Pharmacy Inventory Management System - Main Flask Application
Author: Senior Full Stack Python Developer
Purpose: Backend routes for Dashboard, Inventory CRUD, Billing, and Seasonal Recommendations
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Medicine, Sales, Supplier, init_db
from config import Config
from datetime import datetime, date, timedelta
from sqlalchemy import or_

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_current_season():
    """Returns current season based on month"""
    current_month = datetime.now().month
    return Config.MONTH_TO_SEASON.get(current_month, 'Winter')

def get_dashboard_stats():
    """
    Calculates dashboard statistics
    Returns: dict with total stock, sales today, alerts
    """
    # Total stock count
    total_stock = db.session.query(db.func.sum(Medicine.stock_quantity)).scalar() or 0
    
    # Total sales today
    today = date.today()
    sales_today = db.session.query(db.func.sum(Sales.total_amount)).filter(
        db.func.date(Sales.sale_date) == today
    ).scalar() or 0
    
    # Low stock medicines (< threshold)
    low_stock_medicines = Medicine.query.filter(
        Medicine.stock_quantity < Config.LOW_STOCK_THRESHOLD
    ).all()
    
    # Expiring soon medicines (< 30 days)
    expiring_soon = []
    all_medicines = Medicine.query.all()
    for med in all_medicines:
        if med.is_expiring_soon(Config.EXPIRY_WARNING_DAYS):
            expiring_soon.append(med)
    
    # Seasonal recommendations
    current_season = get_current_season()
    seasonal_medicines = Medicine.query.filter(
        Medicine.seasonal_tag == current_season,
        Medicine.stock_quantity < 50  # Recommend stocking if low
    ).limit(10).all()
    
    return {
        'total_stock': int(total_stock),
        'sales_today': round(sales_today, 2),
        'low_stock_count': len(low_stock_medicines),
        'expiring_count': len(expiring_soon),
        'low_stock_medicines': low_stock_medicines,
        'expiring_medicines': expiring_soon,
        'seasonal_medicines': seasonal_medicines,
        'current_season': current_season
    }

# ============================================================================
# ROUTES - DASHBOARD
# ============================================================================

@app.route('/')
@app.route('/dashboard')
def dashboard():
    """
    Homepage - Shows inventory summary and critical alerts
    Displays: Total Stock, Sales Today, Expiring Medicines, Low Stock Alerts
    """
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

# ============================================================================
# ROUTES - INVENTORY MANAGEMENT (CRUD)
# ============================================================================

@app.route('/inventory')
def inventory():
    """
    Inventory page - Shows all medicines with search functionality
    """
    # Get search query if provided
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Search by name, manufacturer, or category
        medicines = Medicine.query.filter(
            or_(
                Medicine.name.ilike(f'%{search_query}%'),
                Medicine.manufacturer.ilike(f'%{search_query}%'),
                Medicine.category.ilike(f'%{search_query}%')
            )
        ).order_by(Medicine.name).all()
    else:
        # Show all medicines
        medicines = Medicine.query.order_by(Medicine.name).all()
    
    return render_template('inventory.html', medicines=medicines, search_query=search_query)

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_medicine():
    """
    Add new medicine to inventory
    """
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            manufacturer = request.form.get('manufacturer')
            category = request.form.get('category')
            price = float(request.form.get('price'))
            stock_quantity = int(request.form.get('stock_quantity'))
            expiry_date_str = request.form.get('expiry_date')
            
            # Parse expiry date
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            
            # Assign seasonal tag based on category
            seasonal_tag = None
            for season, categories in Config.SEASONAL_CATEGORIES.items():
                if category in categories:
                    seasonal_tag = season
                    break
            
            # Create new medicine
            new_medicine = Medicine(
                name=name,
                manufacturer=manufacturer,
                category=category,
                price=price,
                stock_quantity=stock_quantity,
                expiry_date=expiry_date,
                seasonal_tag=seasonal_tag
            )
            
            db.session.add(new_medicine)
            db.session.commit()
            
            flash(f'✓ Medicine "{name}" added successfully!', 'success')
            return redirect(url_for('inventory'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error adding medicine: {str(e)}', 'danger')
            return redirect(url_for('add_medicine'))
    
    # GET request - show form
    categories = list(set([cat for cats in Config.SEASONAL_CATEGORIES.values() for cat in cats]))
    categories.sort()
    return render_template('add_medicine.html', categories=categories)

@app.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
def edit_medicine(id):
    """
    Edit existing medicine details
    """
    medicine = Medicine.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Update fields
            medicine.name = request.form.get('name')
            medicine.manufacturer = request.form.get('manufacturer')
            medicine.category = request.form.get('category')
            medicine.price = float(request.form.get('price'))
            medicine.stock_quantity = int(request.form.get('stock_quantity'))
            expiry_date_str = request.form.get('expiry_date')
            medicine.expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            
            # Update seasonal tag
            seasonal_tag = None
            for season, categories in Config.SEASONAL_CATEGORIES.items():
                if medicine.category in categories:
                    seasonal_tag = season
                    break
            medicine.seasonal_tag = seasonal_tag
            
            db.session.commit()
            
            flash(f'✓ Medicine "{medicine.name}" updated successfully!', 'success')
            return redirect(url_for('inventory'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'❌ Error updating medicine: {str(e)}', 'danger')
    
    # GET request - show form with current data
    categories = list(set([cat for cats in Config.SEASONAL_CATEGORIES.values() for cat in cats]))
    categories.sort()
    return render_template('edit_medicine.html', medicine=medicine, categories=categories)

@app.route('/inventory/delete/<int:id>', methods=['POST'])
def delete_medicine(id):
    """
    Delete medicine from inventory
    """
    try:
        medicine = Medicine.query.get_or_404(id)
        medicine_name = medicine.name
        
        db.session.delete(medicine)
        db.session.commit()
        
        flash(f'✓ Medicine "{medicine_name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error deleting medicine: {str(e)}', 'danger')
    
    return redirect(url_for('inventory'))

# ============================================================================
# ROUTES - BILLING SYSTEM
# ============================================================================

@app.route('/billing')
def billing():
    """
    Billing page - Select medicines and generate invoice
    """
    # Get all medicines with stock > 0
    medicines = Medicine.query.filter(Medicine.stock_quantity > 0).order_by(Medicine.name).all()
    return render_template('billing.html', medicines=medicines)

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    """
    Process sale and generate invoice
    Automatically deducts stock from inventory
    """
    try:
        # Get cart data from form (JSON format)
        import json
        cart_data = request.form.get('cart_data')
        
        if not cart_data:
            flash('❌ Cart is empty!', 'danger')
            return redirect(url_for('billing'))
        
        cart_items = json.loads(cart_data)
        
        if not cart_items:
            flash('❌ Cart is empty!', 'danger')
            return redirect(url_for('billing'))
        
        # Process each item in cart
        invoice_items = []
        total_amount = 0
        
        for item in cart_items:
            medicine_id = int(item['medicine_id'])
            quantity = int(item['quantity'])
            
            # Get medicine
            medicine = Medicine.query.get(medicine_id)
            
            if not medicine:
                flash(f'❌ Medicine ID {medicine_id} not found!', 'danger')
                return redirect(url_for('billing'))
            
            # Check stock availability
            if medicine.stock_quantity < quantity:
                flash(f'❌ Insufficient stock for {medicine.name}! Available: {medicine.stock_quantity}', 'danger')
                return redirect(url_for('billing'))
            
            # Calculate amount
            item_total = medicine.price * quantity
            total_amount += item_total
            
            # Deduct stock
            medicine.stock_quantity -= quantity
            
            # Record sale
            sale = Sales(
                medicine_id=medicine.id,
                quantity_sold=quantity,
                total_amount=item_total
            )
            db.session.add(sale)
            
            # Add to invoice items
            invoice_items.append({
                'name': medicine.name,
                'quantity': quantity,
                'price': medicine.price,
                'total': item_total
            })
        
        # Commit all changes
        db.session.commit()
        
        # Generate invoice number
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        invoice_date = datetime.now().strftime('%d-%b-%Y %I:%M %p')
        
        flash(f'✓ Invoice generated successfully! Total: ₹{total_amount:.2f}', 'success')
        
        return render_template('invoice.html',
                             invoice_number=invoice_number,
                             invoice_date=invoice_date,
                             items=invoice_items,
                             total_amount=total_amount)
        
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error generating invoice: {str(e)}', 'danger')
        return redirect(url_for('billing'))

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/seasonal_recommendations')
def api_seasonal_recommendations():
    """
    API endpoint for seasonal recommendations
    Returns JSON data
    """
    current_season = get_current_season()
    medicines = Medicine.query.filter(
        Medicine.seasonal_tag == current_season
    ).limit(20).all()
    
    return jsonify({
        'season': current_season,
        'recommendations': [m.to_dict() for m in medicines]
    })

@app.route('/api/medicine/<int:id>')
def api_medicine_details(id):
    """
    API endpoint to get medicine details
    """
    medicine = Medicine.query.get_or_404(id)
    return jsonify(medicine.to_dict())

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# ============================================================================
# TEMPLATE FILTERS
# ============================================================================

@app.template_filter('currency')
def currency_filter(value):
    """Format number as currency"""
    return f"₹{value:,.2f}"

@app.template_filter('days_until')
def days_until_filter(date_value):
    """Calculate days until a date"""
    if isinstance(date_value, str):
        date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
    delta = date_value - date.today()
    return delta.days

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SMART PHARMACY INVENTORY MANAGEMENT SYSTEM")
    print("="*60)
    print("🏥 Starting Flask application...")
    print("📍 Access the application at: http://localhost:5000")
    print("="*60 + "\n")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
