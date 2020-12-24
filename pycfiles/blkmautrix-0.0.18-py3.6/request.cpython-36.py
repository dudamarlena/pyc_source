# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/errors/request.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 4807 bytes
from typing import Optional, Dict, Type, Callable
from .base import MatrixError

class MatrixRequestError(MatrixError):
    __doc__ = 'An error that was returned by the homeserver.'
    http_status: int
    message: Optional[str]
    errcode: str


class MatrixUnknownRequestError(MatrixRequestError):
    __doc__ = 'An unknown error type returned by the homeserver.'

    def __init__(self, http_status=0, text='', errcode=None, message=None):
        super().__init__(f"{http_status}: {text}")
        self.http_status = http_status
        self.text = text
        self.errcode = errcode
        self.message = message


class MatrixStandardRequestError(MatrixRequestError):
    __doc__ = 'A standard error type returned by the homeserver.'
    errcode: str = None

    def __init__(self, http_status, message=''):
        super().__init__(message)
        self.http_status = http_status
        self.message = message


MxSRE = Type[MatrixStandardRequestError]
ec_map = {}
ec_map: Dict[(str, MxSRE)]

def standard_error(code: str) -> Callable[([MxSRE], MxSRE)]:

    def decorator(cls):
        cls.errcode = code
        ec_map[code] = cls
        return cls

    return decorator


def make_request_error(http_status: int, text: str, errcode: str, message: str) -> MatrixRequestError:
    """
    Determine the correct exception class for the error code and create an instance of that class
    with the given values.

    Args:
        http_status: The HTTP status code.
        text: The raw response text.
        errcode: The errcode field in the response JSON.
        message: The error field in the response JSON.
    """
    try:
        ec_class = ec_map[errcode]
        return ec_class(http_status, message)
    except KeyError:
        return MatrixUnknownRequestError(http_status, text, errcode, message)


@standard_error('M_FORBIDDEN')
class MForbidden(MatrixStandardRequestError):
    pass


class MatrixInvalidToken(MatrixStandardRequestError):
    pass


@standard_error('M_UNKNOWN_TOKEN')
class MUnknownToken(MatrixInvalidToken):
    pass


@standard_error('M_MISSING_TOKEN')
class MMissingToken(MatrixInvalidToken):
    pass


class MatrixBadRequest(MatrixStandardRequestError):
    pass


class MatrixBadContent(MatrixBadRequest):
    pass


@standard_error('M_BAD_JSON')
class MBadJSON(MatrixBadContent):
    pass


@standard_error('M_NOT_JSON')
class MNotJSON(MatrixBadContent):
    pass


@standard_error('M_NOT_FOUND')
class MNotFound(MatrixStandardRequestError):
    pass


@standard_error('M_LIMIT_EXCEEDED')
class MLimitExceeded(MatrixStandardRequestError):
    pass


@standard_error('M_UNKNOWN')
class MUnknown(MatrixStandardRequestError):
    pass


@standard_error('M_UNRECOGNIZED')
class MUnrecognized(MatrixStandardRequestError):
    pass


@standard_error('M_UNAUTHORIZED')
class MUnauthorized(MatrixStandardRequestError):
    pass


@standard_error('M_USER_IN_USE')
class MUserInUse(MatrixStandardRequestError):
    pass


@standard_error('M_INVALID_USERNAME')
class MInvalidUsername(MatrixStandardRequestError):
    pass


@standard_error('M_ROOM_IN_USE')
class MRoomInUse(MatrixStandardRequestError):
    pass


@standard_error('M_INVALID_ROOM_STATE')
class MInvalidRoomState(MatrixStandardRequestError):
    pass


@standard_error('M_UNSUPPORTED_ROOM_VERSION')
class MUnsupportedRoomVersion(MatrixStandardRequestError):
    pass


@standard_error('M_INCOMPATIBLE_ROOM_VERSION')
class MIncompatibleRoomVersion(MatrixStandardRequestError):
    pass


@standard_error('M_BAD_STATE')
class MBadState(MatrixStandardRequestError):
    pass


@standard_error('M_GUEST_ACCESS_FORBIDDEN')
class MGuestAccessForbidden(MatrixStandardRequestError):
    pass


@standard_error('M_CAPTCHA_NEEDED')
class MCaptchaNeeded(MatrixStandardRequestError):
    pass


@standard_error('M_CAPTCHA_INVALID')
class MCaptchaInvalid(MatrixStandardRequestError):
    pass


@standard_error('M_MISSING_PARAM')
class MMissingParam(MatrixBadRequest):
    pass


@standard_error('M_INVALID_PARAM')
class MInvalidParam(MatrixBadRequest):
    pass


@standard_error('M_TOO_LARGE')
class MTooLarge(MatrixBadRequest):
    pass


@standard_error('M_EXCLUSIVE')
class MExclusive(MatrixStandardRequestError):
    pass