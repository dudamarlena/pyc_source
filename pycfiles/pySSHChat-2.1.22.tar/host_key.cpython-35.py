# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vlad/source/pySSHChat/pysshchat/lib/host_key.py
# Compiled at: 2018-03-31 11:21:58
# Size of source mod 2**32: 435 bytes
import os
from pathlib import Path
from Crypto.PublicKey import RSA

def genkey(path='~/.ssh/pysshchat'):
    key_path = os.path.expanduser(path)
    path = Path(key_path)
    if not path.is_file():
        Path(path.parent).mkdir(parents=True, exist_ok=True)
        pem = RSA.generate(2048)
        with open(key_path, 'w') as (out):
            out.write(pem.decode('utf-8'))
        print('Generate host key')
    return key_path