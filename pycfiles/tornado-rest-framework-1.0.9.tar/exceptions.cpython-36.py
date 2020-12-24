# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/exceptions.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 5271 bytes
from rest_framework.utils import status
from rest_framework.core.translation import lazy_translate as _
from rest_framework.utils.transcoder import force_text

class TornadoRuntimeWarning(RuntimeWarning):
    pass


class CompressorError(Exception):
    __doc__ = '\n    压缩异常\n    '


class UnicodeDecodeException(UnicodeDecodeError):

    def __init__(self, obj, *args):
        self.obj = obj
        (UnicodeDecodeError.__init__)(self, *args)

    def __str__(self):
        original = UnicodeDecodeError.__str__(self)
        return '%s. You passed in %r (%s)' % (original, self.obj, type(self.obj))


class ImproperlyConfigured(Exception):
    __doc__ = '配置异常'


class FieldError(Exception):
    __doc__ = '字段异常'


class FieldDoesNotExist(Exception):
    __doc__ = '\n    字段在model不存在\n    '


class SkipFieldError(Exception):
    __doc__ = '\n    可跳过的字段异常\n    '


class SkipFilterError(Exception):
    __doc__ = '\n    可跳过的过滤字段异常\n    '


class HTTPError(Exception):

    def __init__(self, status_code=500):
        self.status_code = status_code


def _get_error_details(data, default_code=None):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    if isinstance(data, list):
        ret = [_get_error_details(item, default_code) for item in data]
        return ret
    else:
        if isinstance(data, dict):
            ret = {key:_get_error_details(value, default_code) for key, value in data.items()}
            return ret
        text = force_text(data)
        code = getattr(data, 'code', default_code)
        return ErrorDetail(text, code)


def _get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    else:
        if isinstance(detail, dict):
            return {key:_get_codes(value) for key, value in detail.items()}
        return detail.code


def get_full_details(detail):
    if isinstance(detail, list):
        return [get_full_details(item) for item in detail]
    else:
        if isinstance(detail, dict):
            return {key:get_full_details(value) for key, value in detail.items()}
        return {'message':detail, 
         'code':detail.code}


class ErrorDetail(str):
    __doc__ = '\n    A string-like object that can additionally\n    '
    code = None

    def __new__(cls, string, code=None):
        self = super(ErrorDetail, cls).__new__(cls, string)
        self.code = code
        return self


class APIException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred')
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is None:
            detail = self.default_detail
        self.code = self.default_code if code is None else code
        if status_code is not None:
            self.status_code = status_code
        self.detail = _get_error_details(detail, self.code)

    def __str__(self):
        return '%s' % self.detail

    def get_codes(self):
        """
        Return only the code part of the error details.

        Eg. {"name": ["required"]}
        """
        return _get_codes(self.detail)

    def get_full_details(self):
        """
        Return both the message & code parts of the error details.

        Eg. {"name": [{"message": "This field is required.", "code": "required"}]}
        """
        return get_full_details(self.detail)


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None, params=None, field=None):
        if detail is None:
            detail = self.default_detail
        self.code = self.default_code if code is None else code
        self.field = field
        if params is not None:
            detail %= params
        self.detail = _get_error_details(detail, self.code)

    def __str__(self):
        return str(self.detail)


class ParseError(APIException):
    __doc__ = '\n    解析异常\n    '
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Malformed request')
    default_code = 'parse_error'


class PaginationError(APIException):
    __doc__ = '\n    分页异常\n    '
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid page')
    default_code = 'page_error'


class IllegalAesKeyError(Exception):
    __doc__ = '\n    不合法的AESKey\n    '


class EncryptAESError(Exception):
    __doc__ = '\n    AES加密失败\n    '


class DecryptAESError(Exception):
    __doc__ = '\n    AES解密失败\n    '


class EncodeBase64Error(Exception):
    __doc__ = '\n    Base64编码失败\n    '


class DecodeBase64Error(Exception):
    __doc__ = '\n    Base64解码失败\n    '


class EncodeHexError(Exception):
    __doc__ = '\n    16进制编码失败\n    '


class DecodeHexError(Exception):
    __doc__ = '\n    16进制解码失败\n    '


class RouteConfigurationError(Exception):
    pass


class ReverseNotFound(Exception):
    pass


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    pass