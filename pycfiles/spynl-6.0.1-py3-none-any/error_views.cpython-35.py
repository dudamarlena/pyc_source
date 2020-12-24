# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/error_views.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 3996 bytes
"""
Error views for 4xx and 5xx HTTP errors
"""
from pyramid.security import ACLDenied
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound, HTTPInternalServerError
from spynl.main.exceptions import SpynlException
from spynl.main.utils import log_error
from spynl.main.locale import SpynlTranslationString as _

def spynl_error(exc, request):
    """
    Handle raised SpynlExceptions.

    Get meta info from the assorted HTTP Error, log information and return
    a typical Spynl response.
    """
    http_exc = exc.http_escalate_as()
    request.response.status = http_exc.status
    request.response.status_int = http_exc.status_int
    request.response.content_type = 'application/json'
    top_msg = "Spynl Error of type %s with message: '%s'."
    message = exc.message
    log_error(exc, request, top_msg, exc.__class__.__name__, message)
    return {'status': 'error', 
     'type': exc.__class__.__name__, 
     'message': message}


def error400(exc, request):
    """
    Handle all HTTPErrors.

    We collect information about the original error as best as possible.
    We log informaton and return a typical Spynl response.
    """
    request.response.status = exc.status
    request.response.status_int = exc.status_int
    request.response.content_type = 'application/json'
    error_type = exc.__class__.__name__
    if isinstance(exc, HTTPNotFound):
        message = _('no-endpoint-for-path', default="No endpoint found for path '${path}'.", mapping={'path': request.path_info})
    else:
        if isinstance(exc, HTTPForbidden) and hasattr(exc, 'result') and exc.result is not None:
            if isinstance(exc.result, ACLDenied):
                message = _('permission-denial', default="Permission to '${permission}' ${context} was denied.", mapping={'context': request.context.__class__.__name__, 
                 'permission': exc.result.permission})
                emeta = exc.result
            else:
                message = exc.result.msg
        else:
            if isinstance(exc, HTTPInternalServerError):
                message = _('internal-server-error', default='An internal server error occured.')
            else:
                message = exc.explanation
                if exc.detail:
                    if ':' in exc.detail:
                        error_type, message = exc.detail.split(':', 1)
                else:
                    message = exc.detail
    if error_type.endswith('Exception'):
        error_type = error_type[:-len('Exception')]
    top_msg = "HTTP Error of type %s with message: '%s'."
    log_error(exc, request, top_msg, error_type, message)
    response = {'status': 'error', 'type': error_type, 'message': message}
    if hasattr(exc, 'details') and exc.details:
        response['details'] = exc.details
    return response


def error500(exc, request):
    """
    Handle all failures we do not anticipate in error.

    Give back json, set the error status to 500,
    and only include minimal information (to decrease attack vector).
    However, we log all information we can about the error for debugging.
    """
    request.response.status_int = 500
    request.response.content_type = 'application/json'
    message = str(exc)
    if not message:
        message = _('no-message-available', default='No message available.')
    error_type = exc.__class__.__name__
    if error_type.endswith('Exception'):
        error_type = error_type[:-len('Exception')]
    top_msg = "Server Error (500) of type '%s' with message: '%s'."
    log_error(exc, request, top_msg, error_type, message)
    message = _('internal-server-error', default='An internal server error occured.')
    return dict(status='error', message=message)