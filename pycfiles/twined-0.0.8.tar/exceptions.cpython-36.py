# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/octue/twined/twined/exceptions.py
# Compiled at: 2020-01-10 06:36:33
# Size of source mod 2**32: 1364 bytes


class TwineException(Exception):
    __doc__ = ' All exceptions raised by the twine framework inherits from TwineException'


class InvalidTwine(TwineException):
    __doc__ = ' Raised when the specified twine is invalid\n    '


class MissingTwine(TwineException):
    __doc__ = ' Raised when the specified twine file is not present\n    '


class InvalidInput(TwineException):
    __doc__ = ' Raised when an object is instantiated or a function called with invalid inputs\n    '


class FolderNotPresent(InvalidInput):
    __doc__ = ' Raised when a required folder (e.g. <data_dir>/input) cannot be found\n    '


class ManifestNotFound(InvalidInput):
    __doc__ = ' Raised when a multi manifest can not be refined to a single manifest in a search\n    '


class InvalidManifest(InvalidInput):
    __doc__ = ' Raised when a manifest loaded from JSON does not pass validation\n    '


class InvalidManifestType(InvalidManifest):
    __doc__ = " Raised when user attempts to create a manifest of a type other than 'input', 'output' or 'build'\n    "


class NotImplementedYet(TwineException):
    __doc__ = ' Raised when you attempt to use a function whose high-level API is in place, but which is not implemented yet\n    '


class UnexpectedNumberOfResults(TwineException):
    __doc__ = ' Raise when searching for a single data file (or a particular number of data files) and the number of results exceeds that expected\n    '