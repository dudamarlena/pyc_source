# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tidal_dl\decryption.py
# Compiled at: 2019-08-18 23:21:57
# Size of source mod 2**32: 1730 bytes
"""
@File    :   decryption.py
@Time    :   2019/02/27
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   HIGH Quality Track Dectyption;File From Project 'RedSea'
"""
import base64
from Crypto.Cipher import AES
from Crypto.Util import Counter

def decrypt_security_token(security_token):
    """
    Decrypts security token into key and nonce pair

    security_token should match the securityToken value from the web response
    """
    master_key = 'UIlTTEMmmLfGowo/UC60x2H45W6MdGgTRfo/umg4754='
    master_key = base64.b64decode(master_key)
    security_token = base64.b64decode(security_token)
    iv = security_token[:16]
    encrypted_st = security_token[16:]
    decryptor = AES.new(master_key, AES.MODE_CBC, iv)
    decrypted_st = decryptor.decrypt(encrypted_st)
    key = decrypted_st[:16]
    nonce = decrypted_st[16:24]
    return (
     key, nonce)


def decrypt_file(file, key, nonce):
    """
    Decrypts an encrypted MQA file given the file, key and nonce
    """
    counter = Counter.new(64, prefix=nonce, initial_value=0)
    decryptor = AES.new(key, (AES.MODE_CTR), counter=counter)
    with open(file, 'rb') as (eflac):
        flac = decryptor.decrypt(eflac.read())
        with open(file, 'wb') as (dflac):
            dflac.write(flac)