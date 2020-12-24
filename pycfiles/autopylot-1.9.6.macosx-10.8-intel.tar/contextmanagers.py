# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/autopylot/lib/python2.7/site-packages/autopylot/django/contextmanagers.py
# Compiled at: 2013-11-26 22:17:25
from contextlib import contextmanager
from django.core.cache import cache
from requests.exceptions import Timeout
import json, logging, requests
logger = logging.getLogger('caldwellpy')

@contextmanager
def get_cached(cache_key, data_source, default=None, expire=86400, timeout=10.0):
    data = cache.get(cache_key)
    if not data:
        try:
            resp = requests.get(data_source, timeout=timeout)
            if resp.status_code == requests.codes.ok:
                try:
                    data = json.loads(resp.text)
                    cache.set(cache_key, data, expire)
                except Exception as e:
                    logger.error('Error initializing cache: %s' % e)

            else:
                logger.error('connection failed for url[%s] code[%s] msg[%s]' % (
                 data_source, resp.status_code, resp.text))
        except Timeout:
            logger.error('connection timeout for url[%s]' % data_source)
        except Exception as e:
            logger.error('connection error[%s]' % e)

    yield data or default