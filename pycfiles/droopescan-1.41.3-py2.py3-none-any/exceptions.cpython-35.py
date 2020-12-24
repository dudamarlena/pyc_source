# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/common/exceptions.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 260 bytes


class FileEmptyException(RuntimeError):
    pass


class CannotResumeException(RuntimeError):
    pass


class UnknownCMSException(RuntimeError):
    pass


class VersionFingerprintFailed(RuntimeError):
    pass


class MissingMajorException(Exception):
    pass