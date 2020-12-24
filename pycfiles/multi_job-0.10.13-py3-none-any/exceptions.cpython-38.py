# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/models/exceptions.py
# Compiled at: 2020-02-01 17:15:03
# Size of source mod 2**32: 420 bytes
"""
Multi-job exceptions
"""
from utils.emojis import FIRE
from utils.colours import fail

class PrettyException(Exception):

    def __init__(self, message):
        pretty_msg = f"\n{FIRE}{fail('Oh my!')}{FIRE}\n{message}"
        super().__init__(pretty_msg)


class ParserValidationError(PrettyException):
    pass


class ConfigNotGiven(PrettyException):
    pass


class ArgumentMissing(PrettyException):
    pass