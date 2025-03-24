from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'Walo_ri_dahkin_hhhhhhhhh'

# Hardcoded credentials (for demonstration purposes only)
CREDENTIALS = {
    "username": "admin",
    "password": "supersecret123"
}

# Maximum allowed failed attempts
MAX_FAILED_ATTEMPTS = 3

@app.route('/')
def index():
    # Reset failed attempts when the user visits the login page
    session.pop('failed_attempts', None)
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Initialize failed attempts counter if it doesn't exist
    if 'failed_attempts' not in session:
        session['failed_attempts'] = 0

    # Check if the user has exceeded the maximum failed attempts
    if session['failed_attempts'] >= MAX_FAILED_ATTEMPTS:
        return jsonify({
            "success": False,
            "message": "Khalik mn web o doz lxi haja akhra. Refresh the page a l3ayan."
        })

    # Validate credentials
    if username == CREDENTIALS['username'] and password == CREDENTIALS['password']:
        # Reset failed attempts on successful login
        session.pop('failed_attempts', None)
        return jsonify({
            "success": True,
            "redirect": "/dashboard"  # Use the correct path for redirection
        })
    else:
        # Increment failed attempts counter
        session['failed_attempts'] += 1
        if session['failed_attempts'] >= MAX_FAILED_ATTEMPTS:
            return jsonify({
                "success": False,
                "message": "Khalik mn web o doz lxi haja akhra. Refresh the page a l3ayan."
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Walo 3ayan. ({MAX_FAILED_ATTEMPTS - session['failed_attempts']} attempts remaining)"
            })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)

