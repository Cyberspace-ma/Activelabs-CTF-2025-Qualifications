# Description :

>Intelligence suggests that this program is designed to validate a special passphrase. Your mission, should you choose to accept it, is to crack this security system and discover the hidden secret within !!

> Author : Mr_Togoo

After analyzing the code, we found the function that compares the real value with the input at address `0x4013CE`. So, I used GDB for this operation:

    1- We open GDB and set a breakpoint at this address.
    2- Run Your input.
    3- Check the value it is compared with.


![image](https://github.com/user-attachments/assets/70606ddd-84ea-436e-aa98-afcbaaef50b1)

And congrats , you got the flag!!!

FLAG : 
>CSP{R3v_1s_4_styl3_0f_l1v1ng}
