# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\cd2\env\lib\site-packages\httplog\decorators.py
# Compiled at: 2016-11-29 02:58:47
from __future__ import absolute_import
from functools import wraps
import json
from .services import is_valid_config, get_httplog_data, get_httplog_config
from .tasks import task_http_log

def handle_exception(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            if func.__name__ == 'process_response':
                return args[2]

    return wrapper


def httplog_handler(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        queryset = func(*args, **kwargs)
        request = args[1]
        if request.data.has_key('operator'):
            request.data.pop('operator')
        if is_valid_config():
            http_log_data = get_httplog_data(request, request.data, queryset)
            http_log_config = get_httplog_config()
            task_http_log(http_log_config, http_log_data, request)
        return queryset

    return func_wrapper