# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellexer/core/util.py
# Compiled at: 2019-04-16 12:30:36
# Size of source mod 2**32: 1099 bytes
import io

class ChainStream(io.RawIOBase):

    def __init__(self, *streams):
        self.leftover = b''
        self.stream_iter = iter(streams)
        try:
            self.stream = next(self.stream_iter)
        except StopIteration:
            self.stream = None

    def readable(self):
        return True

    def _read_next_chunk(self, max_length):
        if self.leftover:
            return self.leftover
        else:
            if self.stream is not None:
                return self.stream.read(max_length).encode()
            return b''

    def readinto(self, b):
        buffer_length = len(b)
        chunk = self._read_next_chunk(buffer_length)
        while len(chunk) == 0:
            try:
                self.stream = next(self.stream_iter)
                chunk = self._read_next_chunk(buffer_length)
            except StopIteration:
                self.stream = None
                return 0

        output, self.leftover = chunk[:buffer_length], chunk[buffer_length:]
        b[:len(output)] = output
        return len(output)