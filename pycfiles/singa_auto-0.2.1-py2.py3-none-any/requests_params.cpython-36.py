# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/utils/requests_params.py
# Compiled at: 2020-04-23 00:15:30
# Size of source mod 2**32: 2241 bytes
from functools import wraps, reduce
from flask import request

class ParameterError(Exception):
    pass


def parser_requests():
    params = dict()
    if request.get_json():
        params['json'] = request.get_json() or {}
    if request.files.to_dict():
        params['files'] = request.files.to_dict()
    if request.form.to_dict():
        params['data'] = request.form.to_dict()
    if request.args:
        params['params'] = {k:v for k, v in request.args.items()}
    return params


def param_check(required_parameters=None):

    def decorator(f):

        @wraps(f)
        def wrapped(*args, **kwargs):
            params = parser_requests()
            if required_parameters:
                for location in required_parameters:
                    for field_name in required_parameters[location]:
                        if required_parameters[location][field_name]:
                            if location not in params:
                                raise ParameterError('{} must be provided in {}'.format(field_name, location))
                            if field_name not in params[location]:
                                raise ParameterError('{} must be provided'.format(field_name))

            combined_params = reduce(lambda d1, d2: dict(d1, **d2), list(params.values()), {})
            return f(args, params=combined_params, **kwargs)

        return wrapped

    return decorator