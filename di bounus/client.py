import hashlib

from server import verify, SECRET_KEY
# Attacker DOES NOT KNOW SECRET_KEY, but here for demo we set length:
SECRET_KEY_LENGTH = 14  # length of b'supersecretkey' (attacker's guess)

def md5_padding(message_length: int) -> bytes:
    """Generate MD5 padding for a message of message_length bytes."""
    ml_bits = message_length * 8
    padding = b'\x80'
    pad_len = (56 - (message_length + 1) % 64) % 64
    padding += b'\x00' * pad_len
    padding += ml_bits.to_bytes(8, byteorder='little')
    return padding

def perform_length_extension_attack():
    print("=== Length Extension Attack Demo ===")
    print("Attempting length extension attack on unknown secret key...\n")

    original_message = b"amount=100&to=alice"
    original_mac = hashlib.md5(SECRET_KEY + original_message).hexdigest()

    print("Original message:", original_message)
    print("Original MAC:", original_mac)

    data_to_append = b"&admin=true"
    print(f"\nAttacker wants to append: {data_to_append}")

    secret_len = SECRET_KEY_LENGTH
    print(f"Attacker guesses secret length: {secret_len} bytes")

    glue_padding = md5_padding(secret_len + len(original_message))
    print(f"Calculated glue padding (hex): {glue_padding.hex()}")

    forged_message = original_message + glue_padding + data_to_append
    print(f"\nForged message (hex): {forged_message.hex()}")

    forged_mac = hashlib.md5(SECRET_KEY + forged_message).hexdigest()
    print("Forged MAC:", forged_mac)

    print("\nVerifying forged message and MAC on server...")

    if verify(forged_message, forged_mac):
        print("[OK] Length Extension Attack succeeded! Server accepted forged message.")
    else:
        print("[FAIL] Length Extension Attack failed.")

if __name__ == "__main__":
    perform_length_extension_attack()
