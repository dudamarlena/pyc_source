# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/development2/ise-python-libraries/intelligence/phishme_intelligence/core/exceptions.py
# Compiled at: 2020-05-04 10:30:57
# Size of source mod 2**32: 1732 bytes
from __future__ import unicode_literals, absolute_import

class PhishMeException(Exception):
    __doc__ = '\n    Basic exception thrown by PhishMe configuration errors\n    '


class PmValidationError(Exception):
    __doc__ = '\n    Exception intended for validating PhishMe Intelligence configuration\n    '


class PmSyncError(Exception):
    __doc__ = '\n    Intended for user issues syncing with API\n    '


class PmConnectionError(Exception):
    __doc__ = '\n    For API connection issues\n    '


class PmAttributeError(Exception):
    __doc__ = '\n    For attribute errors in user specified code\n    '


class PmBadConnectionType(Exception):
    __doc__ = '\n    Invalid connection type passed\n    '


class PmFileError(Exception):
    __doc__ = '\n    Specified file is inaccessible, likely because of permissions issues\n    '


class PmSearchTermError(Exception):
    __doc__ = '\n    A search term being specified is incorrect.\n    '


class PmNotImplemented(NotImplementedError):
    __doc__ = '\n    To show when a user is using the wrong class to create an object\n    '