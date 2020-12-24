# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/nonocaptcha/exceptions.py
# Compiled at: 2018-12-17 12:31:54
# Size of source mod 2**32: 933 bytes
""" Exceptions used in library. """

class nonocaptchaError(Exception):
    __doc__ = ' nonoCAPTCHA base exception. '


class SafePassage(nonocaptchaError):
    __doc__ = ' Raised when all checks have passed. Such as being detected or try\n    again.\n    '


class TryAgain(nonocaptchaError):
    __doc__ = ' Raised when audio deciphering is incorrect and we can try again. '


class ReloadError(nonocaptchaError):
    __doc__ = " Raised when audio file doesn't reload to a new one. "


class DownloadError(nonocaptchaError):
    __doc__ = ' Raised when downloading the audio file errors. '


class ButtonError(nonocaptchaError):
    __doc__ = " Raised when a button doesn't appear. "


class IframeError(nonocaptchaError):
    __doc__ = ' Raised when defacing page times out. '


class PageError(nonocaptchaError):
    __doc__ = ' Raised when loading page times out. '