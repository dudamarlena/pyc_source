# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/enums/CipherType.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 111 bytes
from enum import Enum

class CipherType(Enum):
    Login = 1
    SecureNote = 2
    Card = 3
    Identity = 4