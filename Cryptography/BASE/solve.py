import base64

corrupted_base64 = "Qe0I0UzMtIVMtQjRTMy1SIUdIN30="


prefix = "CSP{"

full_base64 = prefix + corrupted_base64

try:
    decoded_bytes = base64.b64decode(full_base64)
    decoded_flag = decoded_bytes.decode('utf-8', errors='ignore')
    print("Decoded Flag:", decoded_flag)
except Exception as e:
    print("Error:", str(e))
