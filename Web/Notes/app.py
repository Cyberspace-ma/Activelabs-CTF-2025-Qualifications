from flask import Flask, request, render_template, session, redirect, url_for, jsonify, make_response
import hashlib
import re
import os
import random
import string
import html
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)
FLAG = "CSP{XS5_15_ST1LL_D4NG3R0U5_1N_2025}"

# In-memory database for the challenge
users = {
    "admin": {
        "password": hashlib.sha256("Admin_1s_Wh@t_CTF_Players_l1ks_T0SEEE!".encode()).hexdigest(),
        "role": "admin",
        "notes": ["This is the admin account. Don't forget to check the reported comments regularly!"]
    }
}

# Comments storage
comments = []
reported_comments = []

# Enhanced WAF for XSS protection
def waf_filter(content):
    # Block script tags and other dangerous tags
    if re.search(r'<\s*(script|img|iframe|embed|object|link|style|meta)[^>]*>', content, re.IGNORECASE):
        return False
    
    # Allow the content if it passes the filter
    return True

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or users.get(session['username'], {}).get('role') != 'admin':
            return "Access denied", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html', comments=comments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('register.html', error="Username and password are required")
        
        if username in users:
            return render_template('register.html', error="Username already exists")
        
        # Store the new user
        users[username] = {
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "role": "user",
            "notes": []
        }
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]["password"] == hashlib.sha256(password.encode()).hexdigest():
            session['username'] = username
            return redirect(url_for('profile'))
        
        return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    username = session['username']
    user_data = users.get(username, {})
    return render_template('profile.html', username=username, role=user_data.get('role', 'user'), notes=user_data.get('notes', []))

@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    username = session['username']
    note = request.form.get('note')
    
    if note:
        if username in users:
            users[username]["notes"].append(note)
    
    return redirect(url_for('profile'))

@app.route('/add_comment', methods=['POST'])
def add_comment():
    username = session.get('username', 'Anonymous')
    content = request.form.get('content', '')
    
    if not content:
        return redirect(url_for('index'))
    
    # Apply WAF filter
    if not waf_filter(content):
        return render_template('index.html', comments=comments, error="Potentially malicious content detected!")
    
    # "Sanitize" the content but with a vulnerability
    # The vulnerability: It allows SVG tags which can execute JavaScript
    sanitized = content
    # Remove script tags but allow SVG and other potentially dangerous tags
    sanitized = re.sub(r'<\s*script[^>]*>.*?<\s*/\s*script\s*>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    
    comment_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    comments.append({
        "id": comment_id,
        "username": username,
        "content": sanitized,
        "raw_content": content
    })
    
    return redirect(url_for('index'))

@app.route('/report_comment/<comment_id>')
def report_comment(comment_id):
    for comment in comments:
        if comment["id"] == comment_id:
            if comment not in reported_comments:
                reported_comments.append(comment)
            return render_template('report_success.html')
    
    return "Comment not found", 404

@app.route('/admin/reports')
@admin_required
def view_reports():
    return render_template('admin_reports.html', reported_comments=reported_comments)

@app.route('/admin/view_comment/<comment_id>')
@admin_required
def view_comment(comment_id):
    for comment in reported_comments:
        if comment["id"] == comment_id:
            # CSRF vulnerability: no CSRF token for the delete action
            return render_template('view_comment.html', comment=comment)
    
    return "Comment not found", 404

@app.route('/admin/delete_comment/<comment_id>')
@admin_required
def delete_comment(comment_id):
    global comments, reported_comments
    
    # Remove from both lists
    comments = [c for c in comments if c["id"] != comment_id]
    reported_comments = [c for c in reported_comments if c["id"] != comment_id]
    
    return redirect(url_for('admin/reports'))

# This endpoint helps simulate admin reviewing reported comments
# In a real CTF, this would be a separate bot or monitoring system
@app.route('/admin/bot')
def admin_bot():
    # Secret endpoint that simulates admin viewing reported content
    # This would typically be triggered by a separate process or worker
    response = make_response(render_template('admin_bot.html', FLAG=FLAG))
    
    # Set special cookie that's only accessible via HttpOnly
    # response.set_cookie('flag', FLAG, httponly=True)
    
    return response

# API endpoint with JSON content that can be used for XSS
@app.route('/api/user_info')
@login_required
def user_info():
    username = session['username']
    user_data = {
        "username": username,
        "role": users.get(username, {}).get('role', 'user')
    }
    
    # Get parameter from request to control output
    callback = request.args.get('callback', '')
    
    # JSONP vulnerability
    if callback:
        # Incomplete validation creates a JSONP vulnerability
        if re.match(r'^[a-zA-Z0-9_]+$', callback):
            return f"{callback}({json.dumps(user_data)})"
    
    return jsonify(user_data)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)