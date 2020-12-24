# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/decorators.py
# Compiled at: 2018-06-20 15:42:58
# Size of source mod 2**32: 1777 bytes
import logging
from flask import request
from mercury_api.exceptions import HTTPError
log = logging.getLogger(__name__)

def validate_json(f):
    """
    Validates the request json body and headers when receiving a POST request.
    """

    def wrapper(*args, **kwargs):
        try:
            if not request.json:
                raise HTTPError('JSON request or mimetype is missing',
                  status_code=400)
        except ValueError:
            body = request.body.read()
            log.debug('JSON request is malformed: {}'.format(body))
            raise HTTPError('JSON request is malformed', status_code=400)

        return f(*args, **kwargs)

    return wrapper


def check_query(f):
    """
    Validates that there is a query dictionary in the request body.
    """

    def wrapper(*args, **kwargs):
        if not isinstance(request.json.get('query'), dict):
            raise HTTPError('JSON request is malformed', status_code=400)
        return f(*args, **kwargs)

    return wrapper