import hashlib


def hash_password(password_string):
    password_hash = hashlib.sha256((password_string).encode('utf8')).hexdigest()
    return password_hash