import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['SECRET_KEY'] = 'icetech-professional-suite-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- DATABASE INITIALIZATION ---
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELS ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(100))
    currency = db.Column(db.String(10), default='USD')
    # Link products to the specific user
    products = db.relationship('Product', backref='owner', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=5)
    image = db.Column(db.String(200), default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES ---

@app.route('/')
@login_required
def dashboard():
    # Only fetch products belonging to the logged-in business
    user_products = Product.query.filter_by(user_id=current_user.id).all()
    
    # Financial Analytics
    total_val = sum(p.price * p.quantity for p in user_products) if user_products else 0
    low_stock = [p for p in user_products if p.quantity <= p.min_stock]
    
    return render_template('dashboard.html', 
                           products=user_products, 
                           total_val=total_val, 
                           low_stock=low_stock)

@app.route('/inventory')
@login_required
def inventory():
    user_products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('inventory.html', products=user_products)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        file = request.files.get('image')
        filename = 'default.jpg'
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_item = Product(
            name=request.form['name'],
            category=request.form['category'],
            price=float(request.form['price']),
            quantity=int(request.form['quantity']),
            min_stock=int(request.form['min_stock']),
            image=filename,
            user_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Product successfully added to your inventory!')
        return redirect(url_for('inventory'))
    return render_template('add.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Prevent duplicate usernames
        existing_user = User.query.filter_by(username=request.form['username']).first()
        if existing_user:
            flash('This username is already taken. Please choose another.')
            return redirect(url_for('register'))
            
        new_user = User(
            username=request.form['username'],
            password=request.form['password'], # In production, use werkzeug.security to hash this!
            business_name=request.form['business_name'],
            currency=request.form['currency']
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

# --- DATABASE CREATION & APP START ---
if __name__ == '__main__':
    with app.app_context():
        # This will create the .db file if it doesn't exist
        db.create_all()
    app.run(debug=True)