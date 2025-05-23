# MAC Forgery Demonstration Using Length Extension Attack

This project demonstrates the difference between a **naive MAC implementation** using `MD5(secret || message)` and a **secure HMAC implementation**, and shows how an attacker can exploit the naive scheme using a length extension attack.

##  Project Structure

.
├── server.py # Server with naive MD5-based MAC (vulnerable)
├── secureserver.py # Server using HMAC-MD5 (secure)
├── attacker.py # Attacker script using hashpumpy to forge MACs
├── attack_attempts.txt # Auto-generated file logging attack results
└── README.md # You're reading it!


---

##  Requirements

- Python 3.x
- `hashpumpy` module  
  Install with:

  ```bash
  pip install hashpumpy

 How to Run the Demo
1. Run the Naive Server

Start the naive server:

python naive_server.py

It will display a legitimate MAC and automatically attempt to verify forged messages from attack_attempts.txt.
2. Run the Attacker Script

In another terminal, run:

python attacker.py

It will:

    Prompt you to paste the MAC intercepted from the server output.

    Try key lengths from 1 to 20 using hashpumpy.

    Save all attempts in attack_attempts.txt.

3. Run the Secure Server (HMAC)

Try verifying the same forged messages with the secure server:

python secure_server.py

You’ll see that all forgery attempts fail because HMAC is not vulnerable to length extension.
 File: attack_attempts.txt

This file is automatically generated by the attacker script and logs each attempt:

Trying key length: 12
Forged message (bytes): b'amount=100&to=alice\x80...\x00&admin=true'
Forged MAC: f41dcfe4b6ea...
----------------------------------------

🔐 Why HMAC Is Safe

Unlike naive MACs (hash(secret || message)), HMAC is specifically designed to avoid structural vulnerabilities of hash functions like MD5. It wraps the message and key in a secure construction that prevents length extension attacks.
🧠 Learning Objectives

    1-Understand the structure of insecure MAC constructions.

    2-Learn about length extension attacks.

    3-Appreciate the security of HMAC over naive hashes.
