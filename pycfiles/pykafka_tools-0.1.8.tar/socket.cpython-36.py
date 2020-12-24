# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/utils/socket.py
# Compiled at: 2017-12-20 01:12:43
# Size of source mod 2**32: 1439 bytes
__doc__ = '\nAuthor: Keith Bourgoin, Emmett Butler\n'
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['recvall_into']
from pykafka.exceptions import SocketDisconnectedError

def recvall_into(socket, bytea, size):
    """
    Reads `size` bytes from the socket into the provided bytearray (modifies
    in-place.)

    This is basically a hack around the fact that `socket.recv_into` doesn't
    allow buffer offsets.

    :type socket: :class:`socket.Socket`
    :type bytea: ``bytearray``
    :type size: int
    :rtype: `bytearray`
    """
    offset = 0
    while offset < size:
        remaining = size - offset
        try:
            chunk = socket.recv(remaining)
        except IOError:
            chunk = None

        if chunk is None or len(chunk) == 0:
            raise SocketDisconnectedError
        bytea[offset:offset + len(chunk)] = chunk
        offset += len(chunk)

    return bytea