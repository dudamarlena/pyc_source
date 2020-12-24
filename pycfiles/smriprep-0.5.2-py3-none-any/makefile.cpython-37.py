# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_vendor/urllib3/packages/backports/makefile.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 1418 bytes
"""
backports.makefile
~~~~~~~~~~~~~~~~~~

Backports the Python 3 ``socket.makefile`` method for use with anything that
wants to create a "fake" socket object.
"""
import io
from socket import SocketIO

def backport_makefile(self, mode='r', buffering=None, encoding=None, errors=None, newline=None):
    """
    Backport of ``socket.makefile`` from Python 3.5.
    """
    if not set(mode) <= {'r', 'w', 'b'}:
        raise ValueError('invalid mode %r (only r, w, b allowed)' % (mode,))
    else:
        writing = 'w' in mode
        reading = 'r' in mode or not writing
        if not reading:
            assert writing
        binary = 'b' in mode
        rawmode = ''
        if reading:
            rawmode += 'r'
        if writing:
            rawmode += 'w'
        raw = SocketIO(self, rawmode)
        self._makefile_refs += 1
        if buffering is None:
            buffering = -1
        if buffering < 0:
            buffering = io.DEFAULT_BUFFER_SIZE
        if buffering == 0:
            if not binary:
                raise ValueError('unbuffered streams must be binary')
            return raw
        if reading and writing:
            buffer = io.BufferedRWPair(raw, raw, buffering)
        else:
            if reading:
                buffer = io.BufferedReader(raw, buffering)
            else:
                assert writing
                buffer = io.BufferedWriter(raw, buffering)
    if binary:
        return buffer
    text = io.TextIOWrapper(buffer, encoding, errors, newline)
    text.mode = mode
    return text