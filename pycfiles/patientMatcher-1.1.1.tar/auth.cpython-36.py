# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/auth/auth.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 700 bytes
import logging, requests, pymongo
from flask import request
LOG = logging.getLogger(__name__)

def authorize(database, request):
    """Validate request's token against database client collection

    Args:
        database(pymongo.database.Database)
        request(request): a request object

    Returns:
        authorized(bool): True or False
    """
    token = request.headers.get('X-Auth-Token')
    query = {'auth_token': token}
    authorized = database['clients'].find_one(query)
    if bool(authorized):
        LOG.info('Authorized client with id "{0}" submits a {1} request'.format(authorized['_id'], request.method))
    return bool(authorized)