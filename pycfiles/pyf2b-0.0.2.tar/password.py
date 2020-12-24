# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/core/password.py
# Compiled at: 2010-05-21 08:57:50
__doc__ = '\nPassword management module that handles the encryption decryption\nfor the stored passwords\n'
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