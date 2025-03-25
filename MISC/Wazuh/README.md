# **Hex Dump & Wazuh SIEM**  

In this challenge, we are given a hex dump that references **Wazuh SIEM**. To solve it, we only need **CyberChef**.  

---

### **Step 1: Analyzing the Hex Dump**  

The provided hex dump contains the following data:  

```
00000000  57 61 7a 75 68 20 69 73 20 61 6e 20 6f 70 65 6e  |Wazuh is an open|
00000010  2d 73 6f 75 72 63 65 20 73 65 63 75 72 69 74 79  |-source security|
00000020  20 6d 6f 6e 69 74 6f 72 69 6e 67 20 70 6c 61 74  | monitoring plat|
00000030  66 6f 72 6d 20 64 65 73 69 67 6e 65 64 20 74 6f  |.........
```  

This translates to readable text about Wazuh. However, there is an **unusual encoded string** hidden within the text.  

---

### **Step 2: Decoding with CyberChef**  

Using **CyberChef**, we can extract and analyze the encoded data.  

![hex dump](https://github.com/user-attachments/assets/e25a4edc-854a-4eee-bdc6-8b03467d4110)

#### **First Layer: Base85 Encoding**  

After copying the encoded text into CyberChef, it **automatically detects and decodes** it using the **Magic (Auto-detect) feature**:  
![base85](https://github.com/user-attachments/assets/a7b094f0-370d-4cfa-9fa6-cbeff38831c6)


#### **Second Layer: Base62 Encoding**  

The output from the first decoding step appears to be **Base62 encoded**. Unlike Base85, **CyberChef's wizard does not auto-detect Base62**, so we need to manually apply the **Base62 decoding operation**:  
![second encryption](https://github.com/user-attachments/assets/0f8d472a-8b5c-466d-abfc-0f4d4d578c40)

---

### **Step 3: Extracting the Flag**  

After applying both decoding steps, we retrieve the flag:  

**`CSP{W4ZUH_1S_my_F4v0r1t3_S1EM}`**  
