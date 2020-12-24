# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rc/exception.py
# Compiled at: 2020-02-24 16:54:39
# Size of source mod 2**32: 842 bytes


class RcException(Exception):
    pass


class MachineCreationException(RcException):
    pass


class MachineDeletionException(RcException):
    pass


class MachineBootupException(RcException):
    pass


class MachineShutdownException(RcException):
    pass


class UploadException(RcException):
    pass


class DownloadException(RcException):
    pass


class SSHException(RcException):
    pass


class MachineNotRunningException(RcException):
    pass


class RunException(RcException):
    pass


class MachineChangeTypeException(RcException):
    pass


class MachineNotReadyException(RcException):
    pass


class SaveImageException(RcException):
    pass


class DeleteImageException(RcException):
    pass


class FirewallRuleCreationException(RcException):
    pass


class FirewallRuleDeleteionException(RcException):
    pass