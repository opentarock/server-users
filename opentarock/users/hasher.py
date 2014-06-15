import binascii

from Crypto.Hash import HMAC, SHA256
from Crypto.Protocol.KDF import PBKDF2


def to_bytes(s):
    if isinstance(s, str):
        return s.encode(encoding='UTF-8')
    return s


class Hasher:
    def hash(self, data, salt):
        def prf(p, s):
            return HMAC.new(p, s, SHA256).digest()
        key = PBKDF2(data, to_bytes(salt), dkLen=16, count=15000, prf=prf)
        return binascii.hexlify(key)
