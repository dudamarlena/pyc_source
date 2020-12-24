# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alforbes/virtualenv/orloclien-py2/lib/python2.7/site-packages/orloclient/_requests.py
# Compiled at: 2017-04-05 08:05:08
from __future__ import print_function
import requests, logging
from .exceptions import ConnectionError, ServerError
__author__ = 'alforbes'
logger = logging.getLogger(__name__)
headers = {'Content-Type': 'application/json'}

def get(*args, **kwargs):
    """ Wrapper for exception handling """
    try:
        logger.debug(('Get args: {}, kwargs: {}').format(args, kwargs))
        return requests.get(headers=headers, *args, **kwargs)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        raise ConnectionError(('Could not connect to Orlo server at {}').format(args[0]))
    except requests.exceptions.RequestException as e:
        logger.debug(e.message)
        raise ServerError(('Could not read from Orlo server, requests raised {}: {}').format(e.__class__.__name__, e.message))


def post(*args, **kwargs):
    """ Wrapper for exception handling """
    try:
        logger.debug(('Post args: {}, kwargs: {}').format(args, kwargs))
        return requests.post(headers=headers, *args, **kwargs)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        raise ConnectionError(('Could not connect to Orlo server at {}').format(args[0]))
    except requests.exceptions.RequestException as e:
        logger.debug(e.message)
        raise ServerError(('Could not read from Orlo server at {u}; requests raised {e}: {m}').format(u=args[0], e=e.__class__.__name__, m=e.message))