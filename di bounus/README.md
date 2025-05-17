
# 🛡️ MAC Forgery Demonstration using MD5

This project demonstrates **Message Authentication Code (MAC)** forgery attempts using **MD5**, showcasing vulnerabilities in naive MAC implementations. It illustrates both secure verification and forged message attacks using direct hash concatenation (`md5(SECRET_KEY + message)`).

## 📁 Project Structure

```
.
├── client.py        # Simulates an attacker forging a message and recomputing the MAC
├── server.py        # (Expected) Insecure MAC implementation using MD5
├── secureserver.py  # (Expected) Secure MAC generation and verification logic
```

## ⚠️ Security Context

This project highlights the weakness of using simple concatenation in MACs:
- `MAC = md5(SECRET_KEY + message)` is vulnerable to forgery and length extension attacks.
- Attackers can:
  - **Intercept a message and its MAC**
  - **Append data** to the message
  - **Reuse or regenerate a forged MAC**

## 🧪 Simulated Files

### `client.py`
- Simulates a **MAC forgery** attempt where the attacker:
  - Recomputes the MAC using the secret key (for demonstration purposes).
  - Demonstrates what would happen if an attacker could guess or calculate a valid MAC.

### `secureserver.py`
- Simulates:
  - A server verifying a legitimate MAC.
  - An attacker reusing the same MAC after appending data (`&admin=true`), **without** access to the key.
  - This demonstrates a **failed** attack due to MAC mismatch, when properly verified.

## 🔐 Intended Learning Outcomes

- Understand the risks of insecure MAC designs (`md5(secret + message)`).
- Learn how forgery attempts can succeed or fail depending on the verification strategy.
- Reinforce the importance of using **HMAC** (e.g., HMAC-SHA256) for secure message authentication.

## ✅ Recommended Fix

Instead of using raw `hashlib.md5(SECRET_KEY + message)`, use `hmac`:

```python
import hmac
import hashlib

def generate_mac(message):
    return hmac.new(SECRET_KEY, message, hashlib.md5).hexdigest()
```

## 🚀 How to Run

Make sure all files (including `server.py` or `secureserver.py`) are in the same directory.

Run the legitimate server simulation and attack reuse test:
```bash
python secureserver.py
```

Run the direct MAC forgery simulation:
```bash
python client.py
```

## 🧠 Notes

- **This project is for educational purposes only.**
- MD5 is deprecated for cryptographic uses—avoid using it in production.
- Use secure algorithms like **HMAC-SHA256** instead of raw hash functions for message authentication.
