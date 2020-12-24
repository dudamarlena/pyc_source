# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/eventloop/posix_utils.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 3312 bytes
from __future__ import unicode_literals
from codecs import getincrementaldecoder
import os, six
__all__ = ('PosixStdinReader', )

class PosixStdinReader(object):
    __doc__ = "\n    Wrapper around stdin which reads (nonblocking) the next available 1024\n    bytes and decodes it.\n\n    Note that you can't be sure that the input file is closed if the ``read``\n    function returns an empty string. When ``errors=ignore`` is passed,\n    ``read`` can return an empty string if all malformed input was replaced by\n    an empty string. (We can't block here and wait for more input.) So, because\n    of that, check the ``closed`` attribute, to be sure that the file has been\n    closed.\n\n    :param stdin_fd: File descriptor from which we read.\n    :param errors:  Can be 'ignore', 'strict' or 'replace'.\n        On Python3, this can be 'surrogateescape', which is the default.\n\n        'surrogateescape' is preferred, because this allows us to transfer\n        unrecognised bytes to the key bindings. Some terminals, like lxterminal\n        and Guake, use the 'Mxx' notation to send mouse events, where each 'x'\n        can be any possible byte.\n    "

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
            return b''
        else:
            try:
                data = os.read(self.stdin_fd, count)
                if data == b'':
                    self.closed = True
                    return ''
            except OSError:
                data = b''

            return self._stdin_decoder.decode(data)