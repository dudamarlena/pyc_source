# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/user/whoami.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 399 bytes
__doc__ = 'system.user.whoami module'
from os import environ
try:
    from os import getuid

    def whoami():
        """whoami function like linux 'whoami' program"""
        with open('/etc/passwd', 'r') as (pwf):
            pwl = pwf.readlines()
        return [u.split(':')[0] for u in pwl if int(u.split(':')[2]) == getuid()][0]


except ImportError:

    def whoami():
        """whoami faker function"""
        return environ['USERNAME']