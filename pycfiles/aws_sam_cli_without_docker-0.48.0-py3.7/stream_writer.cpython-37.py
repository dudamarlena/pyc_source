# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/stream_writer.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 865 bytes
"""
This class acts like a wrapper around output streams to provide any flexibility with output we need
"""

class StreamWriter:

    def __init__(self, stream, auto_flush=False):
        """
        Instatiates new StreamWriter to the specified stream

        Parameters
        ----------
        stream io.RawIOBase
            Stream to wrap
        auto_flush bool
            Whether to autoflush the stream upon writing
        """
        self._stream = stream
        self._auto_flush = auto_flush

    def write(self, output):
        """
        Writes specified text to the underlying stream

        Parameters
        ----------
        output bytes-like object
            Bytes to write
        """
        self._stream.write(output)
        if self._auto_flush:
            self._stream.flush()

    def flush(self):
        self._stream.flush()