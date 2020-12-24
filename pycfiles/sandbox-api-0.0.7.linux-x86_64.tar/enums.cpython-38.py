# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/sandbox_api/enums.py
# Compiled at: 2020-05-04 08:09:32
# Size of source mod 2**32: 234 bytes
from enum import IntEnum, unique

@unique
class SandboxErrCode(IntEnum):
    UNKNOWN = -1
    TIMEOUT = -2
    RESULT_NOT_FOUND = -3
    RESULT_NOT_UTF8 = -4