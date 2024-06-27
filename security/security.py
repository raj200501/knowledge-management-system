import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()

# Example usage
hashed_password = hash_password("my_secure_password")
print(verify_password(hashed_password, "my_secure_password"))
