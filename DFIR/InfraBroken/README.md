### InfraBroken :

# Description :

> An unknown event occurred on my system. I discovered my data on the dark web, but I have no idea how it was leaked from my server. When I checked the outgoing data, I found nothing suspicious. I'm completely confused about this situation and need you to investigate the incident to determine the source of this anomaly.

> Author : Mr_Togoo

> Attachments : [InfraBroken.rar](https://drive.google.com/file/d/1LjQYu_dLOUHKDN_MdJtr_V-zNLEAdQvo/view?usp=sharing) 'InfraBroken.ad1' and 'network.pcapng'

During the analysis of InfraBroken.ad1, we identified a PowerShell script named Fra9syam.ps1:


    1 - Now, we have some data exfiltrated from DNS to 199.36.158.100 with the query "$OutputData.ramadankarim.ma".
    2 - And exfiltrate this OutputData using the malware SuhoorSpy.exe from the following path:
`C:\Users\MrTogoo\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SuhoorSpy.exe`


[![Fra9syam-ps1.png](https://i.postimg.cc/sxsJLWNc/Fra9syam-ps1.png)](https://postimg.cc/hzZxzXgz)


    To extract the `OutputData` using `tshark` from a DNS query, you can use the following command:



[![Outputdata.png](https://i.postimg.cc/mkjSWDxG/Outputdata.png)](https://postimg.cc/SYX9WmNZ)

Let's go back to the PowerShell script. We found that SuhoorSpy.exe transfers data, and upon analyzing it, we discovered that it modifies some characters during the transfer. Specifically, SuhoorSpy.exe performs the following modifications: If `inputData[i]` is 'C', it replaces it with '!'; if 'B', it replaces it with '='; if 'W', it replaces it with '-'; and if '9', it replaces it with '0'. We obtained this output.

`MZqSURdNmp8x2HS4HBd27mACPPptdSPUZ9vjdfD6oBS7YWpbdKi8N7ubNpiJ54E174YNVwAQyZR5zNXMa7ZxwfZCjDkHciKZpnq8UMCc12Azm5pBEuFJtJcCJfos1cGRo5QQFDCPqoWw491j95S9gwkYh8STuKhEqSzTJj37fXaH5bEsAXdcZewX5wopeujVjRgqaY4sxg3od7TwsLH945ZKjTbgBm9K6gufBsrvDbZSYBMW3PwtV5pS4KrBidL2ZVNpza5JfG3uwUR9V`


We put it in CyberChef, and we obtained the flag.


[![lastStep.png](https://i.postimg.cc/qvV7HGL4/lastStep.png)](https://postimg.cc/hfsn9T65)



FLAG : 
>CSP{DN5_G00D_T0_3XF1L7R3_V1A_53CUR3_CH4NN3L5_4ND_L4H_YT9ABL_SY4MNA}
