# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitpeer/exceptions.py
# Compiled at: 2015-11-17 10:40:39
# Size of source mod 2**32: 359 bytes


class NodeDisconnectException(Exception):
    __doc__ = 'This exception is thrown when Protocoin detects a\n    disconnection from the node it is connected.'


class InvalidMessageChecksum(Exception):
    __doc__ = "This exception is thrown when the checksum for a\n    message in a message header doesn't match the actual\n    checksum of the message."