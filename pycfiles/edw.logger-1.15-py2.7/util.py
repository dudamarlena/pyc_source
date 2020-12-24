# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/util.py
# Compiled at: 2018-04-03 08:39:39
""" Utility functions.
"""
from edw.logger.config import LOG_USER_ID
from edw.logger.config import LOG_USER_IP

def get_user_type(name):
    if name == 'Anonymous User':
        return 'Anonymous'
    return 'Authenticated'


def _get_ip(request):
    environ = getattr(request, 'environ', {})
    if 'HTTP_X_FORWARDED_FOR' in environ:
        return environ.get('HTTP_X_FORWARDED_FOR')
    else:
        if 'REMOTE_ADDR' in environ:
            return environ.get('REMOTE_ADDR')
        return environ.get('HTTP_HOST', None)


def _get_user_id(request):
    if request is None:
        request = {}
    user = request.get('AUTHENTICATED_USER', None)
    return getattr(user, 'getUserName', lambda : 'unknown')()


get_ip = _get_ip if LOG_USER_IP else (lambda _: 'ip log disabled')
get_user_id = _get_user_id if LOG_USER_ID else (lambda _: 'user log disabled')

def get_request_data(request):
    if request is not None:
        user_id = get_user_id(request)
        ip = get_ip(request)
        user_type = get_user_type(_get_user_id(request))
        url = request.get('URL', 'NO_URL')
    else:
        user_id = ip = user_type = url = 'NO_REQUEST'
    action = getattr(url, 'split', lambda sep: [''])('/')[(-1)]
    return dict(user=user_id, ip=ip, user_type=user_type, url=url, action=action)