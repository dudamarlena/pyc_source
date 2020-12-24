# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/malicense/lib.py
# Compiled at: 2018-03-25 02:30:13
# Size of source mod 2**32: 1729 bytes
import hashlib, getpass, socket
from .socketcomm import sendMessage

class Unlicensed(Exception):
    pass


def hash_sha256(string):
    """ Returns the hash of string encoded via the SHA-256 algorithm from hashlib"""
    return hashlib.sha256(string.encode()).hexdigest()


def generateHash(licfilename):
    with open(licfilename) as (fx):
        contents = fx.read()
    return hash_sha256(contents)


def rehash(licfilename, hashfilename='.lichash', **kwargs):
    with open(hashfilename, 'w') as (fx):
        fx.write(generateHash(licfilename))


def isLicenseValid(licfilename, hashfilename='.lichash', **kwargs):
    try:
        with open(hashfilename) as (fx):
            assaved = fx.read()
        asgenerated = generateHash(licfilename)
    except IOError:
        pass
    else:
        if asgenerated == assaved:
            return True
        return False


def invalid(warn_with=print, report_to=None, **kwargs):
    """ What to do when the verification fails

        If warn_with == 'raise', an exception will be raised

        example  report_to='120.0.0.1:8000'
    """
    if warn_with is not None:
        if warn_with == 'raise':
            raise Unlicenced('Unlicenced version')
        elif warn_with != False:
            warn_with('Unlicenced version')
    if report_to is not None:
        username = getpass.getuser()
        hostname = socket.gethostname()
        ipaddress = socket.gethostbyname(hostname)
        domainname = socket.getfqdn()
        targethost, port = report_to.split(':')
        sendMessage(targethost, port, username)