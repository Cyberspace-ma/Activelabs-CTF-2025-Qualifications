# **CTI Challenge**  

A cybersecurity company has been making waves with its platform. Can you uncover key details about its origins?  
![logo (2)](https://github.com/user-attachments/assets/76416769-c9e5-496a-8cfa-393130a4e6de)

---

### **Flag Format**  

The flag follows this structure:  

```
CSP{EarliestDomainRegistration_Country_TheirFamousPlatformName_CEOName_EarliestReleaseAvailableVersion_EarliestReleaseAvailableDate}
```

---

### **Step 1: Finding the Domain Registration Date**  

To determine the **earliest domain registration**, we perform a **WHOIS lookup** on `filigran.io`.  
![filigran 1](https://github.com/user-attachments/assets/8fb9d4c1-7564-4eee-9f10-4083aa8e8d6b)

From the lookup, we find that **Filigran.io** was registered on:  

📅 **December 7, 2020**  

🌍 **Country:** **France (fr)**  

**Flag so far:**  
```
CSP{2020-12-07_fr_
```

---

### **Step 2: Identifying Their Famous Platform**  

Filigran is well known for its **OpenCTI** platform.  
![filigran 1](https://github.com/user-attachments/assets/1dd52d04-f2c1-4e41-9c60-3ecb3de89e9a)

**Updated flag:**  
```
CSP{2020-12-07_fr_opencti_
```

---

### **Step 3: Finding the CEO's Name**  

The CEO of **Filigran** is **Samuel Hassine**, confirmed through his **GitHub profile**: [SamuelHassine](https://github.com/SamuelHassine).  

![CEO Name](https://github.com/user-attachments/assets/38bf4682-fd62-4d8a-9702-b86a8b544db8)


**Updated flag:**  
```
CSP{2020-12-07_fr_opencti_samuelhassine_
```

---

### **Step 4: Finding the Earliest Release Version & Date**  

Looking at OpenCTI's **GitHub repository**, we check for the **first commit**, which was made by **Samuel Hassine** on:  
![CEO Name](https://github.com/user-attachments/assets/3844cdda-8109-4eb6-b6e0-d42b4be4703d)


📅 **June 28, 2019**  
🔢 **Version:** **1.0.0**  

**Final flag:**  
```
CSP{2020-12-07_fr_opencti_samuelhassine_1.0.0_2019-06-28}
```
