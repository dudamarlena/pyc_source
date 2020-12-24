# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/exc.py
# Compiled at: 2019-12-26 15:48:50
# Size of source mod 2**32: 2285 bytes
__doc__ = '\nExceptions.\n'
from .status import Status

class CaptchaError(Exception):
    """CaptchaError"""
    status_code = Status.S20_WrongPage.id


class ForbiddenError(Exception):
    """ForbiddenError"""
    status_code = Status.S20_WrongPage.id


class WrongHtmlError(Exception):
    """WrongHtmlError"""
    status_code = Status.S20_WrongPage.id


class DecodeError(Exception):
    """DecodeError"""
    status_code = Status.S25_DecodeError.id


class SoupError(Exception):
    """SoupError"""
    status_code = Status.S30_ParseError.id


class ParseError(Exception):
    """ParseError"""
    code = Status.S30_ParseError.id


class IncompleteDataError(Exception):
    """IncompleteDataError"""
    status_code = Status.S40_InCompleteData.id


class ServerSideError(Exception):
    """ServerSideError"""
    status_code = Status.S60_ServerSideError.id


class DownloadOversizeError(Exception):
    """DownloadOversizeError"""
    pass