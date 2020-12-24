# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breilly/git/fm-orchestrator/module_build_service/errors.py
# Compiled at: 2019-12-12 15:53:56
""" Defines custom exceptions and error handling functions """
from flask import jsonify

class ValidationError(ValueError):
    pass


class Unauthorized(ValueError):
    pass


class Forbidden(ValueError):
    pass


class UnprocessableEntity(ValueError):
    pass


class Conflict(ValueError):
    pass


class NotFound(ValueError):
    pass


class ProgrammingError(ValueError):
    pass


class StreamAmbigous(ValueError):
    pass


class GreenwaveError(RuntimeError):
    pass


def json_error(status, error, message):
    response = jsonify({'status': status, 'error': error, 'message': message})
    response.status_code = status
    return response