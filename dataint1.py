from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import jwt
import datetime
from functools import wraps
import pyotp
import qrcode
import io
import base64
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dataint1'

mysql = MySQL(app)

# Helper: Token Required Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Authorization header is missing!'}), 403
        
        # Expect "Bearer <token>"
        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({'message': 'Invalid Authorization header format!'}), 403
        
        token = parts[1]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token is invalid or expired!'}), 403
        
        return f(current_user, *args, **kwargs)
    return decorated

# 1. User Registration
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data['username']
        password = generate_password_hash(data['password'])
        secret = pyotp.random_base32()

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Users (username, password, twofa_secret) VALUES (%s, %s, %s)', (username, password, secret))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'User registered', '2fa_secret': secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. QR Code for Google Authenticator
@app.route('/qrcode/<username>', methods=['GET'])
def generate_qrcode(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT twofa_secret FROM Users WHERE username = %s', [username])
        user = cur.fetchone()
        cur.close()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        secret = user[0]
        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name='DataInt1')
        qr = qrcode.make(otp_uri)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        qr_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        return jsonify({'qrcode': qr_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. Login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT password FROM Users WHERE username = %s', [username])
        user = cur.fetchone()
        cur.close()

        if not user or not check_password_hash(user[0], password):
            return jsonify({'message': 'Invalid credentials'}), 401

        return jsonify({'message': 'Enter 2FA Code'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. Verify 2FA and Get JWT
@app.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    try:
        data = request.json
        username = data['username']
        code = data['code']

        cur = mysql.connection.cursor()
        cur.execute('SELECT twofa_secret FROM Users WHERE username = %s', [username])
        user = cur.fetchone()
        cur.close()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        totp = pyotp.TOTP(user[0])
        if not totp.verify(code):
            return jsonify({'message': 'Invalid 2FA Code'}), 401

        token = jwt.encode({'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 5. CRUD Operations
@app.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Products')
    products = cur.fetchall()
    cur.close()

    return jsonify(products)

@app.route('/products', methods=['POST'])
@token_required
def add_product(current_user):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO Products (name, description, price, quantity) VALUES (%s, %s, %s, %s)',
                (data['name'], data['description'], data['price'], data['quantity']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product added'})

@app.route('/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute('UPDATE Products SET name=%s, description=%s, price=%s, quantity=%s WHERE id=%s',
                (data['name'], data['description'], data['price'], data['quantity'], product_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product updated'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Products WHERE id = %s', [product_id])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product deleted'})

if __name__ == '__main__':
    app.run(debug=True)
