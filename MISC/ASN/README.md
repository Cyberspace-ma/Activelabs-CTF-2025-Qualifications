### ASN Challenge

In this challenge, we are tasked with performing a quick lookup on an **Autonomous System Number (ASN)**. An ASN provides information about a network’s autonomous system, such as its registration date, IP ranges, owner, and other details. Our goal is to perform a lookup and gather relevant information to identify a product associated with the ASN.

To start, I used **Shodan** with the ASN filter to gather information about the system. The ASN we're focusing on is **AS202053**, which is registered to **CrowdStrike**.

#### Step 1: Shodan Lookup
A quick Shodan lookup reveals some useful details about **AS202053**:

**ASN:** AS202053  
**Owner:** CrowdStrike  
**Top Products & OS:** Nginx and Linux

![Shodan Result](https://github.com/user-attachments/assets/eb94e929-0583-4cc6-8bc3-e97e4431671f)

#### Step 2: Identifying the Flag
From the Shodan results, we can see the top products in use are **Nginx** and **Linux**. Based on this, we can derive the flag.
![2](https://github.com/user-attachments/assets/3a31f284-0dd9-48a1-ad14-d0cf49033c04)


### Flag:
`CSP{Linux_nginx}`
