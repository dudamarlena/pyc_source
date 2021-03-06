# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/views/exceptions.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 2547 bytes
import logging, sys
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import forbidden_view_config
from pyramid.view import notfound_view_config
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound
from oe_utils.validation import ValidationFailure
log = logging.getLogger(__name__)

@view_config(context=Exception, renderer='json', accept='application/json')
def internal_server_error(exception, request):
    log.error((str(exception)), exc_info=(sys.exc_info()))
    request.response.status_int = 500
    return {'message': 'Er ging iets fout in de server. Onze excuses. Stel je fouten vast of heb je een vraag? Mail dan naar ict@onroerenderfgoed.be'}


@notfound_view_config(renderer='json', accept='application/json')
def not_found(request):
    request.response.status_int = 404
    return {'message': 'De door u gevraagde resource kon niet gevonden worden.'}


@view_config(context=NoResultFound, renderer='json')
def failed_no_result_found(exc, request):
    request.response.status_int = 404
    return {'message': 'De door u gevraagde resource kon niet gevonden worden.'}


@view_config(context=HTTPBadRequest, renderer='json', accept='application/json')
def json_bad_request(exc, request):
    request.response.status_int = 400
    return {'message': exc.message}


@view_config(context=ValidationFailure, renderer='json')
def failed_validation(exc, request):
    log.debug(exc.msg)
    log.debug(exc.errors)
    request.response.status_int = 400
    formated_errors = []
    for node in exc.errors:
        formated_errors.append(' '.join(list(reversed(node.split('.')))).capitalize().replace('_', ' ').replace('body', '') + ': ' + exc.errors[node] if node != '' else exc.errors[node])

    return {'message':exc.msg,  'errors':formated_errors}


@forbidden_view_config(accept='application/json', renderer='json')
def forbidden_view(exc, request):
    log.debug('FORBIDDEN anything')
    log.debug(exc)
    log.debug(exc.message)
    log.debug(exc.result)
    if request.authenticated_userid:
        err = {'message':'U bent niet gemachtigd om deze actie uit te voeren.',  'errors':[]}
        if exc.result.msg:
            err['errors'].append(exc.result.msg)
        request.response.status_int = 403
        return err