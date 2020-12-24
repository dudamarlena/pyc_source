# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /sources/github/pyramid_restful_toolkit/pyramid_restful_toolkit/error_handlers.py
# Compiled at: 2014-07-01 00:15:58
# Size of source mod 2**32: 2057 bytes
__author__ = 'tarzan'
from . import ErrorResponse

def _make_error_response(status_code, errors=None, data=None):
    data = {'data': data} if data else {}
    data['error_code'] = status_code
    data['errors'] = errors or {}
    return data


def on_schema_error(context, request):
    """
    :type context: _SchemaError
    :type request: pyramid.request.Request
    """
    request.response.status_code = 400
    return _make_error_response(400, context.autos)


def on_colander_invalid(context, request):
    """
    :type context: colander.Invalid
    :type request: pyramid.request.Request
    """
    request.response.status_code = 400
    return _make_error_response(400, context.asdict())


def on_formencode_invalid(context, request):
    """
    :type context: formencode.Invalid
    :type request: pyramid.request.Request
    """
    request.response.status_code = 400
    return _make_error_response(400, context.unpack_errors())


def on_error_response(context, request):
    """
    :type context: ErrorResponse
    """
    return context.response(request)


def on_deform_validation_failure(context, request):
    """
    :type context: deform.ValidationFailure
    """
    request.response.status_code = 400
    return _make_error_response(400, context.error.asdict())


def includeme(config):
    """
    :type config: pyramid.config.Configurator
    """
    try:
        import formencode
        config.add_view(on_formencode_invalid, context=formencode.Invalid)
    except ImportError:
        pass

    try:
        import colander
        config.add_view(on_colander_invalid, context=colander.Invalid)
    except ImportError:
        pass

    try:
        import schema
        config.add_view(on_schema_error, context=schema.SchemaError)
    except ImportError as e:
        pass

    try:
        import deform
        config.add_view(on_deform_validation_failure, context=deform.ValidationFailure)
    except ImportError as e:
        pass

    config.add_view(on_error_response, context=ErrorResponse)