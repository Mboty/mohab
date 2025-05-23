

# MAC Forgery Demonstration Using Length Extension Attack

This project showcases the **security weaknesses** of a naive MAC implementation (`MD5(secret || message)`) and demonstrates how an attacker can exploit it using a **length extension attack**. It also compares this with a **secure HMAC-based** implementation.

---

## Project Structure

.
├── server.py #  Naive server (vulnerable to length extension)
├── secureserver.py #  Secure server using HMAC
├── client.py #  Attacker script using hashpumpy
├── attack_attempts.txt #  Auto-generated attack log
└── README.md #  This file


---

##  Requirements

- Python 3.x
- [`hashpumpy`](https://pypi.org/project/hashpumpy/) module

Install with:

```bash
pip install hashpumpy

 How to Run the Demo
1️1- Run the Naive Server

Start the insecure server:

python server.py

    Displays the legitimate MAC for a message.

    Reads and verifies forged messages from attack_attempts.txt.

2️2- Run the Attacker Script

In a new terminal, run:

python client.py

This script:

    Prompts for the intercepted MAC.

    Tries key lengths from 1 to 20 using hashpumpy.

    Saves attempts in attack_attempts.txt.

3️3- Run the Secure Server (HMAC)

Run the secure implementation:

python secureserver.py

You’ll observe that:

     All forgery attempts fail
     HMAC is not vulnerable to length extension!

📄 File: attack_attempts.txt

Example contents:

Trying key length: 12
Forged message (bytes): b'amount=100&to=alice\x80...\x00&admin=true'
Forged MAC: f41dcfe4b6ea...
----------------------------------------

🔐 Why HMAC Is Secure

Unlike the naive approach (MD5(secret || message)), HMAC uses a well-defined structure that prevents length extension attacks, even when using insecure hash functions like MD5 or SHA1.
🎓 Learning Objectives

    1- Understand the insecurity of naive MACs.

    2- Learn how length extension attacks work.

    3- Appreciate the design and security of HMAC
