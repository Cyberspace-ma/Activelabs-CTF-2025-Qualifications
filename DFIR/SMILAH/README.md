### SMILAH :

# Description :

> An employee at a mid-sized tech company has gone rogue. They're under pressure from a competitor or a foreign entity to steal sensitive company data—maybe intellectual property, financial data, or customer lists !!!.

> Author : MR_Togoo

> Attachments : [network.pcapng](https://www.mediafire.com/file/tgq5ezu0c7zkvnd/SMILAH.pcapng/file)

During the analysis of the pcap file, we identified a conversation between Mr_Togoo and D@rkshell:

    1 - In the first conversation, the first packet starts with 'a'.
    2 - The second packet begins with the character 'S'.


[![conv1.png](https://i.postimg.cc/Y92HdB0v/conv1.png)](https://postimg.cc/zLQ6fMnN)


    1 - In the second conversation, the last packet starts with 'v'.



[![conv2.png](https://i.postimg.cc/d0jFRVsM/conv2.png)](https://postimg.cc/Lq5G2Rgv)

And these are all the packets:

[![P1.png](https://i.postimg.cc/W39PKYqX/P1.png)](https://postimg.cc/N9rV244H)


[![P2.png](https://i.postimg.cc/C5zVVCjY/P2.png)](https://postimg.cc/ctyzRn95)


[![P3.png](https://i.postimg.cc/Y0ZB243F/P3.png)](https://postimg.cc/sGYNwgbf)

Reassemble the packets and decode using Base64 to reveal the link:

https://drive.google.com/file/d/1X20J8U2BjKHMrBc3fjQ3NxULLMj97Igu/view?usp=sharing

Use `fcrackzip` to find the password and unlock the archive!

[![fcrackzip.png](https://i.postimg.cc/d0YvTyKm/fcrackzip.png)](https://postimg.cc/TKCBzh1p)

FLAG : 
>CSP{N3CESS4RY_T9OL_BSML4H_FM4KLA_:)}
