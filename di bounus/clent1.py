# main.py
from secureserver import verify, SECRET_KEY, generate_mac

def perform_attack():
    intercepted_message = b"amount=100&to=alice"
    intercepted_mac = generate_mac(intercepted_message)  # Attacker gets the original MAC

    data_to_append = b"&admin=true"

    forged_message = intercepted_message + data_to_append
    forged_mac = intercepted_mac  # Attacker tries to reuse the same MAC (simulating an attack)

    print("=== Attacker Simulation ===")
    print("Original message:", intercepted_message.decode())
    print("Original MAC:", intercepted_mac)
    print("Forged message:", forged_message.decode())
    print("Reused MAC (forged MAC):", forged_mac)

    print("\n--- Verifying forged message with reused MAC ---")
    if verify(forged_message, forged_mac):
        print(" MAC verified successfully (attack succeeded!)")
    else:
        print(" MAC verification failed (attack failed)")

def main():
    message = b"amount=100&to=alice"
    mac = generate_mac(message)

    print("=== Server Simulation ===")
    print(f"Original message: {message.decode()}")
    print(f"MAC: {mac}")
    print("\n--- Verifying legitimate message ---")
    if verify(message, mac):
        print("MAC verified successfully. Message is authentic.\n")

    perform_attack()

if __name__ == "__main__":
    main()
