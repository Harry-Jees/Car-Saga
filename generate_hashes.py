import bcrypt

print(bcrypt.hashpw(b'demo123', bcrypt.gensalt()).decode())
print(bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode())
