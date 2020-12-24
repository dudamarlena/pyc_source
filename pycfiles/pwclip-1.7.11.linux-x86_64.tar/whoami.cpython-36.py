# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/user/whoami.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 399 bytes
"""system.user.whoami module"""
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