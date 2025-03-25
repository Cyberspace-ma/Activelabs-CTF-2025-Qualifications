import os
import itertools
import hashlib

def deterministic_random_bytes(seed, size):
    return hashlib.sha256(seed.encode()).digest()[:size]

def generate_variants(label, size):
    unique_values = [deterministic_random_bytes(f"{label}_{i}", size) for i in range(4)]
    return itertools.cycle(unique_values), unique_values

def save_keys_to_file(filename, key_variants):
    with open(filename, "w") as file:
        for idx, variants in enumerate(key_variants, 1):
            file.write(f"Key {idx} variants:\n")
            for variant in variants:
                file.write(variant.hex() + "\n")
            file.write("\n")

key1_cycle, key1_variants = generate_variants("key1", 32)
key2_cycle, key2_variants = generate_variants("key2", 32)
iv1_cycle, iv1_variants = generate_variants("iv1", 16)
iv2_cycle, iv2_variants = generate_variants("iv2", 16)

save_keys_to_file("keys_variants.txt", [key1_variants, key2_variants, iv1_variants, iv2_variants])

for _ in range(8):
    key1 = next(key1_cycle)
    key2 = next(key2_cycle)
    iv1 = next(iv1_cycle)
    iv2 = next(iv2_cycle)
    print(f"Key1: {key1.hex()}\nKey2: {key2.hex()}\nIV1: {iv1.hex()}\nIV2: {iv2.hex()}\n")
