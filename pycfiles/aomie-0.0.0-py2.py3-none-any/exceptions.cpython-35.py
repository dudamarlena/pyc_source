# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/exceptions.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 2518 bytes
__doc__ = 'Exception definitions for aomi'

class AomiError(Exception):
    """AomiError"""
    catmsg = None

    def __init__(self, message=None):
        msg = None
        if self.catmsg is not None and message is not None:
            msg = '%s - %s' % (self.catmsg, message)
        else:
            if self.catmsg is not None:
                msg = self.catmsg
            elif message is not None:
                msg = message
            if msg is not None:
                super(AomiError, self).__init__(msg)
            else:
                super(AomiError, self).__init__()


class AomiCredentials(AomiError):
    """AomiCredentials"""
    catmsg = 'Something wrong with Vault credentials'


class AomiData(AomiError):
    """AomiData"""
    catmsg = 'Invalid aomi data'


class AomiCommand(AomiError):
    """AomiCommand"""
    catmsg = 'Problem with command line arguments'


class AomiFile(AomiError):
    """AomiFile"""
    catmsg = 'Problem with a local file'


class VaultConstraint(AomiError):
    """VaultConstraint"""
    catmsg = 'A Vault Constraint Exists'


class KeybaseAPI(AomiError):
    """KeybaseAPI"""
    catmsg = 'Something wrong with Keybase integration'


class GPG(AomiError):
    """GPG"""
    catmsg = 'Something went wrong interacting with GPG'


class IceFile(AomiError):
    """IceFile"""
    catmsg = 'Corrupt Icefile'


class VaultData(AomiError):
    """VaultData"""
    catmsg = 'Unexpected Vault Data Woe'


class Validation(AomiError):
    """Validation"""
    catmsg = 'Validation Error'
    source = None

    def __init__(self, message=None, source=None):
        super(Validation, self).__init__(message=message)
        self.source = source


class VaultProblem(AomiError):
    """VaultProblem"""
    catmsg = 'Vault Problem'