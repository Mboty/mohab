import hmac
import hashlib

SECRET_KEY = b'supersecretkey'  # The secret key

def generate_mac(message: bytes) -> str:
    # Use HMAC with MD5 to generate MAC
    return hmac.new(SECRET_KEY, message, hashlib.md5).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    expected_mac = generate_mac(message)
    return hmac.compare_digest(mac, expected_mac)  # safer comparison

def main():
    # The original message
    message = b"hellomynameismohab"
    mac = generate_mac(message)

    print("=== Server Simulation ===")
    print(f"Original message: {message.decode()}")
    print(f"MAC: {mac}")
    print("\n--- Verifying legitimate message ---")

    if verify(message, mac):
        print("[OK] MAC verified successfully. Message is authentic.\n")
    else:
        print("[FAIL] MAC verification failed on original message.\n")

    # Now ask user to input a forged MAC
    forged_mac = input("Paste forged MAC to verify: ").strip()

    print("\n--- Verifying forged MAC against original message ---")
    if verify(message, forged_mac):
        print("[WARNING] Forged MAC is valid! (This should NOT happen with proper HMAC)")
    else:
        print("[FAIL] Forged MAC verification failed. HMAC prevents length extension attacks.")

if __name__ == "__main__":
    main()
