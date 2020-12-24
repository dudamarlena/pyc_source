# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\security.py
# Compiled at: 2020-05-09 09:58:17
# Size of source mod 2**32: 4722 bytes
"""Security"""
from base64 import b64encode, b64decode
from uuid import UUID
import random, string, os

def urandom_to_string(length):
    random_bytes = os.urandom(length)
    token = b64encode(random_bytes).decode('utf-8')[:length]
    return token


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    for c in range(10):
        letters = letters + str(c)
    else:
        return ''.join((random.choice(letters) for i in range(stringLength)))


def generateSecureRandomString(stringLength=10):
    """Generate a secure random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits
    return ''.join((secrets.choice(password_characters) for i in range(stringLength)))


def CryptRandInt(length=10):
    """Get random integer in range"""
    r = random.SystemRandom()
    rndint = r.randrange(length)
    return rndint


def CryptRandString(stringLength=10, filters=[]):
    """Generate a random string in a UUID fromat which is crytographically secure and random"""
    bytess = os.urandom(16)
    randomString = UUID(bytes=bytess, version=4).hex
    if 'number' in filters:
        randomString = str(int(randomString, 16))
    else:
        randomString = randomString.upper()
    randomString = randomString[0:stringLength]
    return randomString


def generateCryptographicallySecureRandomString(stringLength=10, filters=[]):
    """Generate a random string in a UUID fromat which is crytographically secure and random"""
    bytess = os.urandom(16)
    randomString = UUID(bytes=bytess, version=4).hex
    if 'number' in filters:
        randomString = str(int(randomString, 16))
    else:
        randomString = randomString.upper()
    randomString = randomString[0:stringLength]
    return randomString