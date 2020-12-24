# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/exceptions.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 2518 bytes
"""Exception definitions for aomi"""

class AomiError(Exception):
    __doc__ = 'Our generic exception. Builds up an appropriate error message for\n    representation to the user'
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
    __doc__ = 'This exception is used for representing errors related to authenticating\n    against a running Vault server'
    catmsg = 'Something wrong with Vault credentials'


class AomiData(AomiError):
    __doc__ = 'Some kind of aomi specific data is invalid'
    catmsg = 'Invalid aomi data'


class AomiCommand(AomiError):
    __doc__ = 'Invalid interaction attempted with the aomi cli'
    catmsg = 'Problem with command line arguments'


class AomiFile(AomiError):
    __doc__ = 'Something is wrong with a file on the local filesystem'
    catmsg = 'Problem with a local file'


class VaultConstraint(AomiError):
    __doc__ = 'Vault is imposing constraints on us. Permission or pathing generally'
    catmsg = 'A Vault Constraint Exists'


class KeybaseAPI(AomiError):
    __doc__ = 'Covers errors related to the keybase API'
    catmsg = 'Something wrong with Keybase integration'


class GPG(AomiError):
    __doc__ = 'Covers errors related to our GPG wrapper'
    catmsg = 'Something went wrong interacting with GPG'


class IceFile(AomiError):
    __doc__ = 'Something is wrong with an aomi generated icefile'
    catmsg = 'Corrupt Icefile'


class VaultData(AomiError):
    __doc__ = 'Something is wrong with data received from Vault. Usually\n    indicates aomi trying to interact with something manually created'
    catmsg = 'Unexpected Vault Data Woe'


class Validation(AomiError):
    __doc__ = 'Some kind of validation failed. Invalid string, length,\n    who knows. Never trust user input tho.'
    catmsg = 'Validation Error'
    source = None

    def __init__(self, message=None, source=None):
        super(Validation, self).__init__(message=message)
        self.source = source


class VaultProblem(AomiError):
    __doc__ = "Something is wrong with Vault itself. Network, sealed,\n    but it's at the point where we can't even validate if\n    the data is there"
    catmsg = 'Vault Problem'