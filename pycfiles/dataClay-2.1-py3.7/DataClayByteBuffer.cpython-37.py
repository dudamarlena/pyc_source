# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/buffer/DataClayByteBuffer.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 391 bytes
""" Class description goes here. """
from io import BytesIO
import dataclay.serialization.python.lang.VLQIntegerWrapper as VLQIntegerWrapper

class DataClayByteBuffer:
    buffer = BytesIO()

    def writeInt(self, i):
        VLQIntegerWrapper().write(buffer, i)