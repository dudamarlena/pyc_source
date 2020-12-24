# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alforbes/src/public/orloclient/orloclient/base_client.py
# Compiled at: 2017-05-08 11:43:10
from __future__ import print_function
import requests, logging
from .exceptions import ConnectionError, ServerError
__author__ = 'alforbes'
logger = logging.getLogger(__name__)

class BaseClient(object):

    def __init__(self, timeout=10, verify_ssl=True):
        self.request_args = {'timeout': timeout, 
           'verify': verify_ssl}
        self.get_headers = {'Content-Type': 'application/json'}

    def _get(self, *args, **kwargs):
        """
        Wraps a GET request with standard parameters
        """
        try:
            req_kw_args = self.request_args.copy()
            req_kw_args.update(kwargs)
            logger.debug(('Get args: {}, kwargs: {}').format(args, req_kw_args))
            return requests.get(headers=self.get_headers, *args, **req_kw_args)
        except (requests.exceptions.ConnectionError,
         requests.exceptions.ConnectTimeout) as e:
            logger.debug(('Requests exception: {}\n{}').format(e.__class__.__name__, e.message))
            raise ConnectionError(('{} while connecting to Orlo server at {}.').format(e.__class__.__name__, args[0]))
        except requests.exceptions.RequestException as e:
            logger.debug(e.message)
            raise ServerError(('Could not read from Orlo server, requests raised {}: {}').format(e.__class__.__name__, e.message))

    def _post(self, *args, **kwargs):
        """
        Wraps a POST request with standard parameters
        """
        try:
            req_kw_args = self.request_args.copy()
            req_kw_args.update(kwargs)
            logger.debug(('Post args: {}, kwargs: {}').format(args, req_kw_args))
            return requests.post(*args, **req_kw_args)
        except (requests.exceptions.ConnectionError,
         requests.exceptions.ConnectTimeout):
            raise ConnectionError(('Could not connect to Orlo server at {}').format(args[0]))
        except requests.exceptions.RequestException as e:
            logger.debug(e.message)
            raise ServerError(('Could not read from Orlo server at {u}; requests raised {e}: {m}').format(u=args[0], e=e.__class__.__name__, m=e.message))