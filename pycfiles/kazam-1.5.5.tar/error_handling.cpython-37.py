# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/pulseaudio/error_handling.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 1064 bytes


class PAError(Exception):
    __doc__ = 'Used for reporting various Pulse Audio Errors'

    def __init__(self, value, msg):
        self.value = value
        self.msg = msg