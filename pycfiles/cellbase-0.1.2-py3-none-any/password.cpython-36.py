# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/password.py
# Compiled at: 2017-05-30 17:25:03
# Size of source mod 2**32: 131 bytes
import hashlib

def hashpassword(text, salt):
    return hashlib.sha512('{0}|{1}'.format(salt, text).encode('utf-8')).hexdigest()