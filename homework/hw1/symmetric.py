from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_key():
    """Generate 256-bit (32-byte) AES key"""
    return os.urandom(32)

def encrypt(key, plaintext):
    """Encrypt using AES-GCM with automatic nonce generation"""
    nonce = os.urandom(12)  # 96-bit nonce for GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return (nonce, ciphertext, encryptor.tag)

def decrypt(key, nonce, ciphertext, tag):
    """Decrypt AES-GCM encrypted message"""
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Test implementation
key = generate_key()
plaintext = b"Confidential company data: Q4 revenue $5.2M"
nonce, ciphertext, tag = encrypt(key, plaintext)
decrypted = decrypt(key, nonce, ciphertext, tag)

print(f"Generated Key: {key.hex()}")
print(f"Original Plaintext: {plaintext}")
print(f"Encrypted Ciphertext: {ciphertext.hex()}")
print(f"Decrypted Plaintext: {decrypted.decode()}")
print(f"Verification: {decrypted == plaintext}")
