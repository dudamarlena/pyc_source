# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/password.py
# Compiled at: 2017-05-30 17:25:03
# Size of source mod 2**32: 131 bytes
import hashlib

def hashpassword(text, salt):
    return hashlib.sha512('{0}|{1}'.format(salt, text).encode('utf-8')).hexdigest()