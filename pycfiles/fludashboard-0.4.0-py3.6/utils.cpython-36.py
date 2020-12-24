# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /storage/Marcelo/codes/FluVigilanciaBR/fludashboard/fludashboard/libs/utils.py
# Compiled at: 2017-10-17 15:31:35
# Size of source mod 2**32: 2581 bytes
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from .episem import episem, extractweekday as extract_weekday
import datetime, os

def calc_last_epiweek(year):
    day = datetime.datetime(int(year), 12, 31)
    day_week = extract_weekday(day)
    if day_week < 3:
        day = day - datetime.timedelta(days=(day_week + 1))
    else:
        day = day + datetime.timedelta(days=(6 - day_week))
    return int(episem(day, out='W'))


def cross_domain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    """

    :see: http://flask.pocoo.org/snippets/56/
    :param origin:
    :param methods:
    :param headers:
    :param max_age:
    :param attach_to_all:
    :param automatic_options:
    :return:
    """
    basestring = str
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None:
        if not isinstance(headers, basestring):
            headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods
        else:
            options_resp = current_app.make_default_options_response()
            return options_resp.headers['allow']

    def decorator(f):

        def wrapped_function(*args, **kwargs):
            if automatic_options:
                if request.method == 'OPTIONS':
                    resp = current_app.make_default_options_response()
                else:
                    resp = make_response(f(*args, **kwargs))
            else:
                if not attach_to_all:
                    if request.method != 'OPTIONS':
                        return resp
                h = resp.headers
                h['Access-Control-Allow-Origin'] = origin
                h['Access-Control-Allow-Methods'] = get_methods()
                h['Access-Control-Max-Age'] = str(max_age)
                if headers is not None:
                    h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


def recursive_dir_name(path: str, steps_back: int):
    """

    :param path:
    :param steps_back:
    :return:
    """
    for _ in range(steps_back):
        path = os.path.dirname(path)

    return path