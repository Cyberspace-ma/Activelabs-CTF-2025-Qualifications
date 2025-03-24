from flask import Flask, render_template, request, redirect, url_for, make_response, session, flash
import os
import secrets
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
DB_PATH = 'ctf_challenge.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    c.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
              ('admin', 'Admin_1s_Wh@hhhhhhhhhhh_CSRF_1s_eaaasy!', 1))
    admin_id = c.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()[0]
    c.execute("INSERT OR IGNORE INTO notes (user_id, title, content) VALUES (?, ?, ?)",
              (admin_id, 'FLAG', 'CSP{Cl13nt_S1d3_Ar3_1ntr3sst1ng_P4rt_0f_W3b_P3nt3st1ng}'))
    
    conn.commit()
    conn.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'is_admin' not in session or not session['is_admin']:
            flash('Admin access required', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('register.html')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'danger')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        user = c.execute("SELECT id, username, password, is_admin FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[3]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    notes = c.execute("SELECT id, title, content FROM notes WHERE user_id = ?", (session['user_id'],)).fetchall()
    conn.close()
    return render_template('dashboard.html', notes=notes)

@app.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('Title and content are required', 'danger')
            return render_template('new_note.html')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)", 
                  (session['user_id'], title, content))
        conn.commit()
        conn.close()
        
        flash('Note created successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('new_note.html')

@app.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    note = c.execute("SELECT id, title, content FROM notes WHERE id = ? AND user_id = ?", 
                     (note_id, session['user_id'])).fetchone()
    conn.close()
    
    if not note:
        flash('Note not found or access denied', 'danger')
        return redirect(url_for('dashboard'))
        
    return render_template('view_note.html', note=note)

@app.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", (note_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Note deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# ===== ADMIN ROUTES =====

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    users = c.execute("SELECT id, username, is_admin FROM users").fetchall()
    conn.close()
    return render_template('admin_panel.html', users=users)

@app.route('/admin/notes')
@login_required
@admin_required
def admin_notes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    notes = c.execute('''
        SELECT notes.id, users.username, notes.title, notes.content 
        FROM notes 
        JOIN users ON notes.user_id = users.id
    ''').fetchall()
    conn.close()
    return render_template('admin_notes.html', notes=notes)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        
        if not new_password:
            flash('New password is required', 'danger')
            return render_template('profile.html')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, session['user_id']))
        conn.commit()
        conn.close()
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('profile'))
        
    return render_template('profile.html')

# ===== API ENDPOINTS =====

@app.route('/api/change_password', methods=['POST'])
def api_change_password():
    username = request.form.get('username')
    new_password = request.form.get('new_password')
    
    if not username or not new_password:
        return {'error': 'Username and new password are required'}, 400
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    user = c.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    
    if not user:
        conn.close()
        return {'error': 'User not found'}, 404
    
    c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    conn.close()
    
    return {'success': True, 'message': 'Password updated successfully'}

@app.route('/profile/change_password', methods=['GET'])
def change_password_form():
    return render_template('change_password.html')

# ===== HEALTHCHECK =====

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)