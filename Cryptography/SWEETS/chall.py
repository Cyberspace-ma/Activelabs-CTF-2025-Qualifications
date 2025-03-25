from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

flag = "CSP{FAKE_FLAG}"
first_part = "FAKE"
second_part = "FLAG"

key1 = "?"
key2 = "?"
iv1 = "?"
iv2 = "?"

cipher1 = AES.new(key1, AES.MODE_CBC, iv1)
encrypted_first = cipher1.encrypt(pad(first_part.encode(), AES.block_size))

cipher2 = AES.new(key2, AES.MODE_CBC, iv2)
encrypted_second = cipher2.encrypt(pad(second_part.encode(), AES.block_size))

with open("flag.enc", "wb") as f:
    f.write(encrypted_first + encrypted_second)
