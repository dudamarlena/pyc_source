# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../multi_job/models/exceptions.py
# Compiled at: 2020-02-14 16:10:01
# Size of source mod 2**32: 486 bytes
"""
Multi-job exceptions
"""
from multi_job.utils.colours import fail
from multi_job.utils.emojis import FIRE

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


class StepError(PrettyException):
    pass