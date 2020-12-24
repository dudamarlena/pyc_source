# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/oneiot_core/env.py
# Compiled at: 2020-04-30 19:44:59
# Size of source mod 2**32: 106 bytes
import os

def var(name, default):
    if os.getenv(name) is not None:
        return os.getenv(name)
    return default