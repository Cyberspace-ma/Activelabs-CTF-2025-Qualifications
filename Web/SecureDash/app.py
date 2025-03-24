from flask import Flask, request, render_template, jsonify, session
import os
import uuid
from functools import wraps
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import base64
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

FLAG = "CSP{SST1_1s_N0t_Th4t_E4sy_R1ght}"

# Simulated user database
users = {
    "admin": {
        "username": "admin",
        "password": str(uuid.uuid4()),
        "role": "admin"
    }
}

# Jinja2 environment setup
env = Environment(loader=FileSystemLoader('templates'))
env.globals['secret_hash'] = lambda x: hashlib.sha256(x.encode()).hexdigest()[:8]

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "Authentication required"}), 401
        username = session["username"]
        user = users.get(username)
        if not user or user.get("role") != "admin":
            return jsonify({"error": "Admin privileges required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if username in users:
        return jsonify({"error": "Username exists"}), 400
    
    users[username] = {"username": username, "password": password, "role": "user"}
    return jsonify({"message": "Registration successful"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({"error": "Invalid credentials"}), 401
    
    session['username'] = username
    return jsonify({"message": "Login successful", "user": {"username": user["username"], "role": user["role"]}}), 200

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    role = users[username]['role']
    return render_template('dashboard.html', username=username, role=role)

@app.route('/preview', methods=['POST'])
@login_required
def preview():
    username = session['username']
    data = request.get_json()
    
    template_str = data.get('template', '')
    if not template_str:
        return jsonify({"error": "Template required"}), 400
    
    try:
        # Obfuscated SSTI vulnerability
        encoded = base64.b64encode(template_str.encode()).decode()
        decoded = base64.b64decode(encoded).decode()
        
        env.filters['obfuscate'] = lambda x: ''.join(chr(ord(c) ^ 0x1) for c in str(x))
        template = env.from_string(decoded)
        context = {
            'username': username,
            'role': users[username]['role'],
            'secret_key': 'REDACTED'
        }
        result = template.render(**context)
        
        return jsonify({"preview": result})
    except Exception as e:
        return jsonify({"error": f"Rendering failed: {str(e)}"}), 400

@app.route('/flag')
@admin_required
def get_flag():
    return jsonify({"flag": FLAG})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60000, debug=False)