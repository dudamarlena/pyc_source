# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/mrlpy/exceptions.py
# Compiled at: 2017-08-11 20:26:07
"""
Module containing exceptions used by mrlpy
"""

class HandshakeTimeout(RuntimeError):
    """
        Handshake with proxy service timed-out.
        This is due to some sort of error in high-level communication between MRL and the this python instance
        Only raised after low-level TCP connection has been established
        """

    def __init__(self, message):
        super(RuntimeError, self).__init__(message)