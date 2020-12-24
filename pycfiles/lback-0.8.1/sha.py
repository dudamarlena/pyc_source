# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sha.pyc
# Compiled at: 2008-01-21 20:55:00
import warnings
warnings.warn('the sha module is deprecated; use the hashlib module instead', DeprecationWarning, 2)
from hashlib import sha1 as sha
new = sha
blocksize = 1
digest_size = 20
digestsize = 20