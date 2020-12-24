# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/req.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 2513 bytes
import re, requests
from functools import wraps
import traceback
from time import sleep
import logging

def retry(retries=3):

    def _retry(func):

        @wraps(func)
        def _wrapper(*args, **kwargs):
            index = 0
            while index < retries:
                index += 1
                try:
                    response = func(*args, **kwargs)
                    status_code = response.status_code
                    if status_code == 200:
                        break
                    else:
                        is_404 = status_code == 404
                        if is_404:
                            _logger = logging.warning
                        else:
                            _logger = logging.error
                        _logger('RESPONSE STATUS CODE : %s' % status_code)
                        if is_404:
                            break
                        else:
                            sleep(1)
                            continue
                except Exception as e:
                    traceback.print_exc()
                    response = None

            return response

        return _wrapper

    return _retry


_get = requests.get
_post = requests.post

def _method(get):

    @retry(5)
    def _(*args, **kwds):
        if 'timeout' not in kwds:
            kwds['timeout'] = 30
        else:
            if 'headers' not in kwds:
                kwds['headers'] = {}
            if 'User-Agent' not in kwds['headers']:
                kwds['headers']['User-Agent'] = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        r = get(*args, **kwds)
        sleep(1)
        return r

    return _


get = _method(_get)
post = _method(_post)
requests.get = get
requests.post = post