# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/core/password.py
# Compiled at: 2010-05-21 08:57:50
"""
Password management module that handles the encryption decryption
for the stored passwords
"""
from base64 import b64encode, b64decode
import pyDes
_key = None

def encrypt(clear_pass):
    """
    returns the base 64 encoded version of the
    encrypted password

    @param clear_pass: the clear_text password, make sure there is no
        trailing blank in it by stipping it before.
    @type clear_pass: string
    """
    my_key = pyDes.triple_des(_key)
    return b64encode(my_key.encrypt(clear_pass, pad=' '))


def decrypt(b64hash):
    """
    returns the decrypted password

    @param b64hash: the base64 encoded hash encrypted in 3-des
    @type b64hash: string
    """
    my_key = pyDes.triple_des(_key)
    return my_key.decrypt(b64decode(b64hash), pad=' ')