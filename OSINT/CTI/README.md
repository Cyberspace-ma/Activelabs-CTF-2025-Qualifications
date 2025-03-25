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

![famous platform](https://github.com/user-attachments/assets/25c5f720-930e-457b-a0be-7962c62b5cdf)


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
![famous platform](https://github.com/user-attachments/assets/d18d7686-8a41-4e68-90bc-b4dbd15effd7)



📅 **June 28, 2019**  
🔢 **Version:** **1.0.0**  

**Final flag:**  
```
CSP{2020-12-07_fr_opencti_samuelhassine_1.0.0_2019-06-28}
```
