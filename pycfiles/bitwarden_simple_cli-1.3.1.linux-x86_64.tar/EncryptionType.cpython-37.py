# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/enums/EncryptionType.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 282 bytes
from enum import Enum

class EncryptionType(Enum):
    AesCbc256_B64 = 0
    AesCbc128_HmacSha256_B64 = 1
    AesCbc256_HmacSha256_B64 = 2
    Rsa2048_OaepSha256_B64 = 3
    Rsa2048_OaepSha1_B64 = 4
    Rsa2048_OaepSha256_HmacSha256_B64 = 5
    Rsa2048_OaepSha1_HmacSha256_B64 = 6