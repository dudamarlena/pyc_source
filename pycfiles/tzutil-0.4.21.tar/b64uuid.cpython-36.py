# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/b64uuid.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 256 bytes
from os import urandom
from base64 import urlsafe_b64encode

def b64uuid():
    return urlsafe_b64encode(urandom(16)).decode('utf-8').rstrip('=')


if __name__ == '__main__':
    import time
    while True:
        print(b64uuid())
        time.sleep(0.5)