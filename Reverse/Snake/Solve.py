import string

# Read the encrypted secret
with open('enc_secret.txt', 'r') as f:
    enc_secret = f.read().strip()

# The same alphabet used in the encryption
new_alphabet = list(string.ascii_lowercase + string.digits + string.punctuation)

# Iterate over all possible mystery_num values (100 to 1000)
for possible_mystery_num in range(100, 1001):
    dec_secret = ''
    current_shift = possible_mystery_num
    valid = True

    for char in enc_secret:
        try:
            index = new_alphabet.index(char)
            # Reverse the shift (subtract instead of add)
            new_index = (index - current_shift) % len(new_alphabet)
            dec_secret += new_alphabet[new_index]
            current_shift += 10  # Increment as in encryption
        except ValueError:
            # Invalid character (not in alphabet), skip this mystery_num
            valid = False
            break
    
    # Check if the decrypted text starts with "CSP{"
    if valid and dec_secret.startswith("csp{"):
        print(f"Found correct mystery_num: {possible_mystery_num}")
        print(f"Decrypted secret: {dec_secret}")
        break  # Stop after finding the first valid flag
else:
    print("No valid flag found. Check the encrypted file or alphabet.")
