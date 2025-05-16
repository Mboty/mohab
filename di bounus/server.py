import hashlib

SECRET_KEY = b'supersecretkey'  # The secret key

def generate_mac(message: bytes) -> str:
    return hashlib.md5(SECRET_KEY + message).hexdigest()  # Hash the message with the secret key

def verify(message: bytes, mac: str) -> bool:
    expected_mac = generate_mac(message)
    return mac == expected_mac

def main():
    # The original message
    message = b"amount=100&to=alice"
    mac = generate_mac(message)
    
    print("=== Server Simulation ===")
    print(f"Original message: {message.decode()}")
    print(f"MAC: {mac}")
    print("\n--- Verifying legitimate message ---")
    
    if verify(message, mac):
        print("MAC verified successfully. Message is authentic.\n")
if __name__ == "__main__":
    main()
