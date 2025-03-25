from Crypto.PublicKey import RSA
import owiener
from Crypto.Util.number import long_to_bytes

with open(r'C:\Users\study\OneDrive - OFPPT\Bureau\assembly\CTF-event\RSA\key.pub', 'r') as f:
    key = RSA.import_key(f.read())

n = key.n
e = key.e

d = owiener.attack(e, n)
print(f"Private exponent d: {d}")

with open(r'flag.enc', 'rb') as f:
    c = int.from_bytes(f.read(), byteorder='big')

m = pow(c, d, n)

decrypted_message = long_to_bytes(m)

print("Raw decrypted message:", decrypted_message)

flag = decrypted_message.split(b'\0')[-1]
print("Decrypted flag:", flag.decode())