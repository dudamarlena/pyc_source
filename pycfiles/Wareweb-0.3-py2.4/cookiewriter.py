# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wareweb/cookiewriter.py
# Compiled at: 2006-10-22 17:17:11
from Cookie import SimpleCookie
import timeinterval, time

class Cookie(object):
    """
    Object that represents a cookie meant to be set.  This is like the
    standard ``Cookie.SimpleCookie`` object, only slightly nicer --
    each cookie object is just one ``name=value`` setting, and dates
    can be given as a few special values (``'ONCLOSE'``, ``'NOW'``,
    ``'NEVER'``, and ``timeinterval`` strings like ``'1w'``).
    """
    __module__ = __name__

    def __init__(self, name, value, path, expires=None, secure=False):
        self.name = name
        self.value = value
        self.path = path
        self.secure = secure
        if expires == 'ONCLOSE' or not expires:
            expires = None
        elif expires == 'NOW' or expires == 'NEVER':
            expires = time.gmtime(time.time())
            if expires == 'NEVER':
                expires = (
                 expires[0] + 10,) + expires[1:]
            expires = time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', expires)
        else:
            if isinstance(expires, (str, unicode)) and expires.startswith('+'):
                interval = timeinterval.time_decode(expires[1:])
                expires = time.time() + interval
            if isinstance(expires, (int, long, float)):
                expires = time.gmtime(expires)
            if isinstance(expires, (tuple, time.struct_time)):
                expires = time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', expires)
        self.expires = expires
        return

    def __repr__(self):
        return '<%s %s=%r>' % (self.__class__.__name__, self.name, self.value)

    def header(self):
        c = SimpleCookie()
        c[self.name] = self.value
        c[self.name]['path'] = self.path
        if self.expires is not None:
            c[self.name]['expires'] = self.expires
        if self.secure:
            c[self.name]['secure'] = True
        return str(c).split(':')[1].strip()