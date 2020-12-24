# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/api_utils.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 3818 bytes
import copy
from flask import request, url_for
from odcs.server.models import Compose

def pagination_metadata(p_query, request_args):
    """
    Returns a dictionary containing metadata about the paginated query.
    This must be run as part of a Flask request.
    :param p_query: flask_sqlalchemy.Pagination object
    :param request_args: a dictionary of the arguments that were part of the
    Flask request
    :return: a dictionary containing metadata about the paginated query
    """
    request_args_wo_page = dict(copy.deepcopy(request_args))
    for key in ['page', 'per_page', 'endpoint']:
        if key in request_args_wo_page:
            request_args_wo_page.pop(key)

    for key in request_args:
        if key.startswith('_'):
            request_args_wo_page.pop(key)

    pagination_data = {'page': p_query.page, 
     'pages': p_query.pages, 
     'per_page': p_query.per_page, 
     'prev': None, 
     'next': None, 
     'total': p_query.total, 
     'first': url_for(request.endpoint, page=1, per_page=p_query.per_page, _external=True, **request_args_wo_page), 
     
     'last': url_for(request.endpoint, page=p_query.pages, per_page=p_query.per_page, _external=True, **request_args_wo_page)}
    if p_query.has_prev:
        pagination_data['prev'] = url_for(request.endpoint, page=p_query.prev_num, per_page=p_query.per_page, _external=True, **request_args_wo_page)
    if p_query.has_next:
        pagination_data['next'] = url_for(request.endpoint, page=p_query.next_num, per_page=p_query.per_page, _external=True, **request_args_wo_page)
    return pagination_data


def filter_composes(flask_request):
    """
    Returns a flask_sqlalchemy.Pagination object based on the request parameters
    :param request: Flask request object
    :return: flask_sqlalchemy.Pagination
    """
    search_query = dict()
    for key in ['owner', 'source_type', 'source', 'state']:
        if flask_request.args.get(key, None):
            search_query[key] = flask_request.args[key]

    query = Compose.query
    if search_query:
        query = query.filter_by(**search_query)
    page = flask_request.args.get('page', 1, type=int)
    per_page = flask_request.args.get('per_page', 10, type=int)
    return query.paginate(page, per_page, False)