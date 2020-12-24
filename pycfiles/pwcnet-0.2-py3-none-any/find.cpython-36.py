# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/user/find.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 665 bytes
__doc__ = 'userfind'
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