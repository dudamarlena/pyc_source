# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/no_cloud/crypto.py
# Compiled at: 2017-03-11 19:27:45
import six
from base64 import urlsafe_b64encode
from hashlib import md5, pbkdf2_hmac
from cryptography.fernet import Fernet, InvalidToken

def fernet_encrypt(message, password):
    if isinstance(password, six.text_type):
        password = password.encode('utf-8')
    password = md5(password).hexdigest()
    if isinstance(password, six.text_type):
        password = password.encode('utf-8')
    password = urlsafe_b64encode(password)
    return Fernet(password).encrypt(message)


def fernet_decrypt(message, password):
    if isinstance(password, six.text_type):
        password = password.encode('utf-8')
    password = md5(password).hexdigest()
    if isinstance(password, six.text_type):
        password = password.encode('utf-8')
    password = urlsafe_b64encode(password)
    try:
        return Fernet(password).decrypt(message)
    except InvalidToken:
        raise AssertionError('invalid decryption password')


def sha512_hash(message, salt, iterations=100000):
    if isinstance(message, six.text_type):
        message = message.encode('utf-8')
    if isinstance(salt, six.text_type):
        salt = salt.encode('utf-8')
    return pbkdf2_hmac('sha512', message, salt, iterations)


def digest(hashed, characters, length=16):
    if six.PY2:
        hashed = [ ord(b) for b in hashed ]
    digest = ''
    characters_length = len(characters)
    for c in hashed[-length:]:
        if c >= characters_length:
            c = c % characters_length
        digest += characters[c]

    return digest