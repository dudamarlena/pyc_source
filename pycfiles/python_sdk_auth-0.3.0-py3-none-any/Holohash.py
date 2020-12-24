# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/HologramAuth/Holohash.py
# Compiled at: 2019-10-24 15:30:15
# Size of source mod 2**32: 2039 bytes
import binascii
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
__XOR__ = lambda x, y: bytes([x ^ y])

class Holohash:

    def __init__(self):
        pass

    def __parse_sim_milenage_at_response(self, resp):
        resp = resp[:-6]
        sres_length = int(resp[:2]) * 2
        sres = binascii.unhexlify(resp[2:sres_length + 2])
        resp = resp[sres_length + 2:]
        kc_length = int(resp[:2]) * 2
        kcstr = resp[2:kc_length + 2]
        kc = binascii.unhexlify(kcstr)
        kc = kc[:-1] + bytes([kc[(-1)] & 252])
        return (sres, kc)

    def generate_milenage_token(self, response, device_time):
        sres, kc = self._Holohash__parse_sim_milenage_at_response(response)
        hmac_key2 = ((sres + kc) * 3)[:32]
        return self._Holohash__hmac_sha256(key=hmac_key2, msg=device_time)

    def generate_sim_gsm_milenage_command(self, imsi, iccid, nonce, device_time):
        nonce = binascii.unhexlify(nonce)
        hmac_key = self._Holohash__logical_xor(((imsi + iccid) * 6).encode('ascii'), nonce)
        rand_parts = binascii.unhexlify(self._Holohash__hmac_sha256(key=hmac_key, msg=device_time))
        print(f"len: {len(rand_parts)}")
        rand_part_1 = rand_parts[:len(rand_parts) // 2]
        rand_part_2 = rand_parts[len(rand_parts) // 2:]
        rand = self._Holohash__logical_xor(rand_part_1, rand_part_2)
        return binascii.hexlify(rand).decode().upper()

    def __logical_xor(self, buf1, buf2):
        return ''.join((__XOR__(x, y) for x, y in zip(buf1, buf2)))

    def __hmac_sha256(self, key, msg):
        hasher = HMAC.new(key=key, msg=(msg.encode('ascii')), digestmod=SHA256)
        return hasher.hexdigest()