# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-65c3rg8f/urllib3/urllib3/packages/backports/makefile.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 1418 bytes
__doc__ = '\nbackports.makefile\n~~~~~~~~~~~~~~~~~~\n\nBackports the Python 3 ``socket.makefile`` method for use with anything that\nwants to create a "fake" socket object.\n'
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
        reading = 'r' in mode or 
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
        elif reading:
            buffer = io.BufferedReader(raw, buffering)
        else:
            assert writing
            buffer = io.BufferedWriter(raw, buffering)
    if binary:
        return buffer
    text = io.TextIOWrapper(buffer, encoding, errors, newline)
    text.mode = mode
    return text