# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/foxtrot-api-client/lib/python3.4/site-packages/foxtrot/_required_fields.py
# Compiled at: 2015-05-24 07:16:54
# Size of source mod 2**32: 513 bytes
from functools import wraps
from .errors import ParameterError

def check_required(f):

    @wraps(f)
    def wrapper(instance, data):
        required = globals()[f.__name__]()
        for param in required:
            if param not in data:
                raise ParameterError(param)
                continue

        return f(instance, data)

    return wrapper


def optimize():
    return [
     'file_url', 'file_name', 'geocode', 'stop_name', 'date_starting',
     'warehouse', 'num_drivers', 'num_avg_service_time', 'float_fuel_cost',
     'float_driver_wage', 'float_mpg']