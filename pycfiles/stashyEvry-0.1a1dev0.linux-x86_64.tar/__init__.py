# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/e210990/bin/python26/lib/python2.6/site-packages/stashy/__init__.py
# Compiled at: 2014-06-25 10:41:27
__version__ = '0.1'
from .client import Stash

def connect(url, username, password, verify=True):
    """Connect to a Stash instance given a username and password.

    This is only recommended via SSL. If you need are using
    self-signed certificates, you can use verify=False to ignore SSL
    verifcation.
    """
    return Stash(url, username, password, verify)


__all__ = [
 'connect']