import hashlib
import os
import ast

SECRET_KEY = b'supersecretkey'  # secret, unknown to attacker

def generate_mac(message: bytes) -> str:
    # Naive MAC: MD5(secret_key || message)
    return hashlib.md5(SECRET_KEY + message).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    expected_mac = generate_mac(message)
    return mac == expected_mac

def main():
    message = b"amount=100&to=alice"
    mac = generate_mac(message)

    print("=== Server Simulation ===")
    print(f"Original message: {message.decode()}")
    print(f"MAC: {mac}")

    print("\n--- Verifying legitimate message ---")
    if verify(message, mac):
        print("MAC verified successfully. Message is authentic.\n")
## Attacker attempts
    attack_file = "attack_attempts.txt"
    if not os.path.exists(attack_file):
        print(f"")
        return

    with open(attack_file, "r") as f:
        lines = f.readlines()

    current_message = None
    current_mac = None
    current_key_len = None

    for line in lines:
        line = line.strip()

        if line.startswith("Trying key length"):
            try:
                current_key_len = int(line.split(":")[1].strip())
            except Exception as e:
                print(f"Error parsing key length: {e}")
                current_key_len = None

        elif line.startswith("Forged message"):
            try:
                message_str = line.split(":", 1)[1].strip()
                current_message = ast.literal_eval(message_str)
                if not isinstance(current_message, bytes):
                    print("Error: Forged message must be bytes.")
                    current_message = None
            except Exception as e:
                print(f"Error parsing forged message: {e}")
                current_message = None

        elif line.startswith("Forged MAC"):
            current_mac = line.split(":", 1)[1].strip()

        # If all values are set, try to verify the message
        if current_message and current_mac and current_key_len is not None:
            print(f"\n--- Verifying forged message (Key length: {current_key_len}) ---")
            print(f"Forged message: {current_message}")
            print(f"Forged MAC: {current_mac}")
            if verify(current_message, current_mac):
                print("MAC verified successfully . Attack succeeded")
            else:
                print("MAC verification failed , Attack failed")
            # Reset for next attempt
            current_message = None
            current_mac = None
            current_key_len = None

if __name__ == "__main__":
    main()
