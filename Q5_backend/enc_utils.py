from cryptography.fernet import Fernet

def create_enc_key(enc_key_path):
    key = Fernet.generate_key()
    with open(enc_key_path, 'wb') as outfile:
        outfile.write(key)

def read_enc_key_file(enc_key_path):
    with open(enc_key_path, 'rb') as infile:
        key = infile.read()

    return key

def encrypt_passwd(passwd, enc_key):
    f = Fernet(enc_key)
    return f.encrypt(passwd.encode())

def decrypt_passwd(enc_passwd, enc_key):
    f = Fernet(enc_key)
    return f.decrypt(enc_passwd).decode()