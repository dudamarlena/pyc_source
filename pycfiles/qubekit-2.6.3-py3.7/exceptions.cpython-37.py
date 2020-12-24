# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/utils/exceptions.py
# Compiled at: 2019-09-23 09:51:08
# Size of source mod 2**32: 1115 bytes


class OptimisationFailed(Exception):
    __doc__ = "\n    Raise for seg faults from PSI4 - geomeTRIC/Torsiondrive/QCEngine interactions.\n    This should mean it's more obvious to users when there's a segfault.\n    "


class HessianCalculationFailed(Exception):
    __doc__ = '\n\n    '


class TorsionDriveFailed(Exception):
    __doc__ = '\n\n    '


class PickleFileNotFound(Exception):
    __doc__ = '\n    Cannot find .QUBEKit_states.\n    '


class QUBEKitLogFileNotFound(Exception):
    __doc__ = '\n    Cannot find QUBEKit_log.txt. This is only raised when a recursive search fails.\n    '


class FileTypeError(Exception):
    __doc__ = '\n    Invalid file type e.g. trying to read a mol file when we only accept pdb or mol2.\n    '


class TopologyMismatch(Exception):
    __doc__ = '\n    This indicates that the topology of a file does not match the stored topology.\n    '


class ChargemolError(Exception):
    __doc__ = '\n    Chargemol did not execute properly.\n    '


class Psi4Error(Exception):
    __doc__ = '\n    Psi4 did not execute properly\n    '