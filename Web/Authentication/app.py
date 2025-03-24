from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
import jwt
import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecret@2025'
SECRET_KEY = 'rednut123_'


# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route('/')
def home():
    username = session.get('username')
    jwt_token = request.args.get('token')
    if username:
        conn = get_db_connection()
        history = conn.execute('SELECT * FROM auth_history WHERE username = ?', (username,)).fetchall()
        conn.close()
        return render_template('index.html', username=username, history=history, token=jwt_token)

    return render_template('index.html', username=None, token=jwt_token)


# Admin page
@app.route('/admin')
def admin_page():
    token = request.headers.get('Authorization')
    
    if token:
        token = token.split(" ")[1]
    print(f"Received token: {token}")

    if not token:
        flash('Access denied. You are not admin', 'error')
        return render_template('error.html', message='No way hhhhhh')

    try:
        # Fixed: Properly verify the JWT signature with the correct secret key
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f"Decoded token: {decoded_token}")

        # Extract the role from the decoded token
        role = decoded_token.get('role')
        print(f"User role: {role}")

        if role != 'admin':
            flash('Access denied. You do not have admin rights.', 'error')
            return render_template('error.html', message='Access denied. You do not have admin rights.')

        return render_template('admin.html')

    except jwt.ExpiredSignatureError:
        flash('Your session has expired. Please log in again.', 'error')
        return render_template('error.html', message='Your session has expired. Please log in again.')
    except jwt.InvalidTokenError:
        flash('Invalid token. Please log in again.', 'error')
        return render_template('error.html', message='Invalid token. Please log in again.')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and user['password'] == password:
            conn.execute('INSERT INTO auth_history (username, event, timestamp) VALUES (?, ?, ?)',
                         (username, 'Login Successful', datetime.datetime.utcnow()))
            conn.commit()
            conn.close()

            session['username'] = username
            # Generate JWT token upon successful login
            token = jwt.encode({'username': username, 'role': user['role'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                               SECRET_KEY, algorithm='HS256')

            flash(f'Welcome back, {username}! You have successfully logged in.', 'success')
            # Redirect to the homepage with the JWT token in the URL
            return redirect(url_for('home', token=token))

        conn.close()
        flash('Incorrect username or password. Please verify your credentials and try again.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        # Check if username already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            conn.close()
            return redirect(url_for('register'))

        # Insert new user into the database
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, 'user'))
        conn.commit()
        conn.close()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Logout
@app.route('/logout')
def logout():
    username = session.pop('username', None)
    if username:
        conn = get_db_connection()
        conn.execute('INSERT INTO auth_history (username, event, timestamp) VALUES (?, ?, ?)',
                     (username, 'Logout Successful', datetime.datetime.utcnow()))
        conn.commit()
        conn.close()

    flash('You have successfully logged out. See you soon!', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)