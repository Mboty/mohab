# attack.py
import hashlib
from server import verify, SECRET_KEY  # Import from the server

def perform_attack():
    intercepted_message = b"amount=100&to=alice"
    intercepted_mac = hashlib.md5(SECRET_KEY + intercepted_message).hexdigest()  # Attacker got this

    data_to_append = b"&admin=true"

    # Attacker does not know the key, but here we use it for testing
    forged_message = intercepted_message + data_to_append
    forged_mac = hashlib.md5(SECRET_KEY + forged_message).hexdigest()

    print("=== Attacker Simulation ===")
    print("Forged message:", forged_message.decode())
    print("Forged MAC:", forged_mac)

    print("\n--- Check forged message ---")
    if verify(forged_message, forged_mac):
        print("MAC check passed (attack worked).")
    else:
        print("MAC check failed (attack failed).")

if __name__ == "__main__":
    perform_attack()
