from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open("flag.enc", "rb") as f:
    encrypted_data = f.read()

encrypted_first = encrypted_data[:32]
encrypted_second = encrypted_data[32:64]

key1 = bytes.fromhex("76f0d5e6ee66476fc9efe72606c60068c94bacb2f9b07c3e34c80dfeedf1778e")
key2 = bytes.fromhex("6addf3aa7e6bd99651de39a181d2bfaee51d46460120a70a4f7c611792dfaa0a")
iv1 = bytes.fromhex("d51fad3192f73024aa356e148d8e7d72")
iv2 = bytes.fromhex("a8593a21673e232682a16bfcf995c28c")

cipher1 = AES.new(key1, AES.MODE_CBC, iv1)
decrypted_first = unpad(cipher1.decrypt(encrypted_first), AES.block_size).decode()

cipher2 = AES.new(key2, AES.MODE_CBC, iv2)
decrypted_second = unpad(cipher2.decrypt(encrypted_second), AES.block_size).decode()

flag = f"CSP{{{decrypted_first}_{decrypted_second}}}"
print("Flag:", flag)