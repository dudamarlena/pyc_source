# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spl/errors.py
# Compiled at: 2016-12-14 12:10:02
# Size of source mod 2**32: 506 bytes
from enum import Enum

class ExitCode(Enum):
    OK = 0
    UNKNOWN_COMMAND = 1
    CANNOT_GET_STATE_LOCK = 2
    NON_SINGLETON_RESULT = 3
    UNINSTALLABLE = 4
    NOT_INSTALLED = 5
    ALREADY_ENABLED = 6
    ALREADY_DISABLED = 7


class NonSingletonResultException(Exception):
    exit_code = ExitCode.NON_SINGLETON_RESULT


class CannotGetStateLockException(Exception):
    exit_code = ExitCode.CANNOT_GET_STATE_LOCK


class NotDownloadableException(Exception):
    exit_code = ExitCode.UNINSTALLABLE