# **QR Communication Challenge**  

This challenge was straightforward and required only **CyberChef** for decoding.  

---

### **Step 1: Scanning the QR Code**  

Upon scanning the QR code, we obtain **five different encoded parts** of text. Each part contributes to forming the final flag.  

---

### **Step 2: Decoding Each Part**  

The five segments appear to be encoded in different formats. Let’s decode them one by one using **CyberChef**:  

| Encoded Part | Encoding Type | Decoded Text |
|-------------|--------------|--------------|
| `INJVA===` | **Base32** | `CSP` |
| `MC0rM{WO9[` | **Base92** | `{QR_C0D3` |
| `_NER_` | **Rot13** | `_ARE_` |
| `52 33 34 4c 4c 59 5f` | **Hex** | `R34LLY_` |
| `QlI0SU5GVUNLfQ==` | **Base64** | `BR4INFUCK}` |

---

### **Step 3: Constructing the Flag**  

By combining all the decoded parts, we get:  

**`CSP{QR_C0D3_ARE_R34LLY_BR4INFUCK}`**  

---

### **Conclusion**  

This challenge was simple and required:  
1. **Scanning the QR Code**  
2. **Identifying encoding methods** for each part  
3. **Using CyberChef** to decode them  
4. **Reassembling the flag**  
