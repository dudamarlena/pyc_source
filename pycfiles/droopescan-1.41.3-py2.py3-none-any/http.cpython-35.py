# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/common/http.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 283 bytes
try:
    from http import cookiejar
except ImportError:
    import cookielib as cookiejar

class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda *args, self, **args: False
    netscape = True
    rfc2965 = hide_cookie2 = False