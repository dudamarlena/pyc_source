# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/flask-magic/flask_magic/exceptions.py
# Compiled at: 2016-04-06 20:48:42
# Size of source mod 2**32: 740 bytes
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from werkzeug.exceptions import HTTPException

class ApplicationError(Exception):
    pass


class ModelError(ApplicationError):
    pass


class UserError(ApplicationError):
    pass


class ViewError(ApplicationError):
    pass


class MailmanConfigurationError(HTTPException):
    code = 500
    description = 'MAIL is not configured properly'


class MailmanUnknownProviderError(HTTPException):
    code = 500
    description = 'MAIL is configured with an unknown provider'


class SQLAlchemyError(OperationalError, HTTPException):
    code = 500
    description = 'DB Error'