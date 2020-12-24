# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/data/stream_buffer.py
# Compiled at: 2017-02-13 07:58:24
# Size of source mod 2**32: 178 bytes


class StreamBuffer:

    def __init__(self):
        self.buffer = []

    def insert(self, data):
        self.buffer.append(data)

    def get(self):
        return self.buffer