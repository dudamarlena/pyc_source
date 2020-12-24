# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/errors.py
# Compiled at: 2010-07-21 06:59:33
"""Error Definitions

...
"""
from circuits.web.exceptions import HTTPException

class WikiError(HTTPException):
    """Base class for all error pages."""
    traceback = False


class ForbiddenErr(WikiError):
    code = 403


class NotFoundErr(WikiError):
    code = 404


class UnsupportedMediaTypeErr(WikiError):
    code = 415


class NotImplementedErr(WikiError):
    code = 501
    description = '<p>This feature has not yet been implemented.Please come back and try again later.</p>'


class ServiceUnavailableErr(WikiError):
    code = 503