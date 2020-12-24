# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/requests_ntlm/ntlm/des.py
# Compiled at: 2013-08-26 10:52:44
import des_c

class DES:
    des_c_obj = None

    def __init__(self, key_str):
        """"""
        k = str_to_key56(key_str)
        k = key56_to_key64(k)
        key_str = ''
        for i in k:
            key_str += chr(i & 255)

        self.des_c_obj = des_c.DES(key_str)

    def encrypt(self, plain_text):
        """"""
        return self.des_c_obj.encrypt(plain_text)

    def decrypt(self, crypted_text):
        """"""
        return self.des_c_obj.decrypt(crypted_text)


DESException = 'DESException'

def str_to_key56(key_str):
    """"""
    if type(key_str) != type(''):
        pass
    if len(key_str) < 7:
        key_str = key_str + '\x00\x00\x00\x00\x00\x00\x00'[:7 - len(key_str)]
    key_56 = []
    for i in key_str[:7]:
        key_56.append(ord(i))

    return key_56


def key56_to_key64(key_56):
    """"""
    key = []
    for i in range(8):
        key.append(0)

    key[0] = key_56[0]
    key[1] = key_56[0] << 7 & 255 | key_56[1] >> 1
    key[2] = key_56[1] << 6 & 255 | key_56[2] >> 2
    key[3] = key_56[2] << 5 & 255 | key_56[3] >> 3
    key[4] = key_56[3] << 4 & 255 | key_56[4] >> 4
    key[5] = key_56[4] << 3 & 255 | key_56[5] >> 5
    key[6] = key_56[5] << 2 & 255 | key_56[6] >> 6
    key[7] = key_56[6] << 1 & 255
    key = set_key_odd_parity(key)
    return key


def set_key_odd_parity(key):
    """"""
    for i in range(len(key)):
        for k in range(7):
            bit = 0
            t = key[i] >> k
            bit = (t ^ bit) & 1

        key[i] = key[i] & 254 | bit

    return key