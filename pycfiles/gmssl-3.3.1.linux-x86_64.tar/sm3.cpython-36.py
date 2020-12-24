# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/sm3.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 420 bytes
from .libsm3 import lib_sm3, sm3_hash
if lib_sm3 is None:
    from .sm3_implement import *
    using_libsm3 = False
else:
    from .libsm3 import *
    using_libsm3 = True
assert sm3_hash(b'01').upper() == '7f4528abbaeb75420d8ae5842f12b221deb73722d49e02fccb461450e0c1d7ad'.upper()