# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/posix_utils.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 3312 bytes
from __future__ import unicode_literals
from codecs import getincrementaldecoder
import os, six
__all__ = ('PosixStdinReader', )

class PosixStdinReader(object):
    """PosixStdinReader"""

    def __init__(self, stdin_fd, errors='ignore' if six.PY2 else 'surrogateescape'):
        assert isinstance(stdin_fd, int)
        self.stdin_fd = stdin_fd
        self.errors = errors
        self._stdin_decoder_cls = getincrementaldecoder('utf-8')
        self._stdin_decoder = self._stdin_decoder_cls(errors=errors)
        self.closed = False

    def read(self, count=1024):
        """
        Read the input and return it as a string.

        Return the text. Note that this can return an empty string, even when
        the input stream was not yet closed. This means that something went
        wrong during the decoding.
        """
        if self.closed:
            return ''
        else:
            try:
                data = os.read(self.stdin_fd, count)
                if data == '':
                    self.closed = True
                    return ''
            except OSError:
                data = ''

            return self._stdin_decoder.decode(data)