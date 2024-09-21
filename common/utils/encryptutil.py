import base64
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT


def base64_encode(b):
    if isinstance(b, str):
        b = b.encode()
    return base64.b64encode(b).decode()


def base64_decode(b):
    if isinstance(b, str):
        b = b.encode()
    return base64.b64decode(b)


def encrypt(value, key='78FA3AFA7485409A'):
    crypt_sm4 = CryptSM4()
    if isinstance(key, str):
        key = key.encode()
    if isinstance(value, str):
        value = value.encode()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    s = crypt_sm4.crypt_ecb(value)
    return base64_encode(s)


def decrypt(value, key='78FA3AFA7485409A'):
    crypt_sm4 = CryptSM4()
    if isinstance(key, str):
        key = key.encode()
    if isinstance(value, str):
        value = value.encode()
    crypt_sm4.set_key(key, SM4_DECRYPT)
    s = crypt_sm4.crypt_ecb(base64_decode(value))
    return s.decode()
