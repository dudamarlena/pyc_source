# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/security.py
# Compiled at: 2019-09-03 16:41:08
# Size of source mod 2**32: 89 bytes
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['argon2'])