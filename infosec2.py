from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/infosec2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Use environment variables in production

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ----------------------- Database Models -----------------------

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pname = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# ----------------------- Authentication Routes -----------------------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id), expires_delta=datetime.timedelta(minutes=10))
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

# ----------------------- Product Operations -----------------------

@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.json
    new_product = Product(
        pname=data['pname'],
        description=data.get('description', ''),
        price=float(data['price']),  # Ensure price is correctly handled
        stock=int(data['stock'])
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    products_list = [
        {'pid': p.pid, 'pname': p.pname, 'description': p.description, 'price': str(p.price), 'stock': p.stock}
        for p in products
    ]
    return jsonify(products_list)

@app.route('/products/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.json
    product.pname = data.get('pname', product.pname)
    product.description = data.get('description', product.description)
    product.price = float(data.get('price', product.price))
    product.stock = int(data.get('stock', product.stock))
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    product = Product.query.get(pid)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

# ----------------------- Run Application -----------------------

if __name__ == '__main__':
    app.run(debug=True)