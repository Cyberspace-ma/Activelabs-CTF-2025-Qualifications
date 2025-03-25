from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long


flag = b"CSP{Y0u_4r3_R34lly_G00d_1n_Crypt0!}"


with open(r'C:\Users\study\OneDrive - OFPPT\Bureau\assembly\CTF-event\RSA\key.pub', 'r') as f:
    key = RSA.import_key(f.read())


n = key.n
e = key.e

m = bytes_to_long(flag)

c = pow(m, e, n)

with open('flag.enc', 'wb') as f:
    f.write(c.to_bytes((c.bit_length() + 7) // 8, byteorder='big'))

print("Flag encrypted and saved to flag.enc")