# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mando/neurospaces_project/sspy/source/snapshots/0/build/lib/sspy/errors.py
# Compiled at: 2011-09-15 17:42:41
"""!

This file contains all of the exception objects used
to handle errors.
"""
from exceptions import Exception

class CompileError(Exception):
    pass


class ConnectError(Exception):
    pass


class InputError(Exception):
    pass


class OutputError(Exception):
    pass


class ParameterSetError(Exception):
    pass


class PluginDirectoryError(Exception):
    pass


class PluginFileError(Exception):
    pass


class PluginError(Exception):
    pass


class RuntimeError(Exception):
    pass


class ScheduleeError(Exception):
    pass


class ScheduleeCreateError(Exception):
    pass


class ScheduleError(Exception):
    pass


class SolverError(Exception):
    pass


class ServiceError(Exception):
    pass