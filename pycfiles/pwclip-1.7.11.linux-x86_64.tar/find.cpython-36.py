# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/user/find.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 665 bytes
"""userfind"""
import sys

def userfind(pattern='1000', mode='user'):
    """
        userfind function:
        >>> 0 = user
        >>> 1 = x
        >>> 2 = uid
        >>> 3 = gid
        >>> 4 = comment
        >>> 5 = home
        >>> 6 = shell
        """
    pfmap = {'user':0, 
     'x':1, 
     'uid':2, 
     'gid':3, 
     'comment':4, 
     'home':5, 
     'shell':6}
    mode = int(pfmap[mode])
    pstr = str(pattern)
    try:
        with open('/etc/passwd', 'r') as (pwd):
            hits = [f.split(':') for f in [l for l in pwd.readlines() if pstr in l]]
            if hits:
                return hits[0][mode]
    except PermissionError as err:
        return False