import hashlib

SECRET_KEY = b'supersecretkey'  # Unknown to attacker

def generate_mac(message: bytes) -> str:
    return hashlib.md5(SECRET_KEY + message).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    return generate_mac(message) == mac

def main():
    msg = b"amount=100&to=alice"
    mac = generate_mac(msg)
    print("Server Original message:", msg)
    print("Server Original MAC:", mac)
    if verify(msg, mac):
        print("Server Verification succeeded.\n")
    else:
        print("Server Verification failed.\n")

if __name__ == "__main__":
    main()
