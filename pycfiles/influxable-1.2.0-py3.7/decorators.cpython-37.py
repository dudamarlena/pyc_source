# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/decorators.py
# Compiled at: 2019-10-23 08:36:50
# Size of source mod 2**32: 1659 bytes
import json, requests
from . import exceptions

def raise_if_error(func):

    def func_wrapper(*args, **kwargs):
        try:
            request = args[0]
            params = kwargs.get('params', {})
            res = func(*args, **kwargs)
            try:
                json_res = res.json()
            except json.decoder.JSONDecodeError:
                json_res = {}

            res.raise_for_status()
        except requests.exceptions.MissingSchema as err:
            try:
                raise exceptions.InfluxDBInvalidURLError(request.base_url)
            finally:
                err = None
                del err

        except requests.exceptions.ConnectionError as err:
            try:
                raise exceptions.InfluxDBConnectionError(err)
            finally:
                err = None
                del err

        except requests.exceptions.HTTPError as err:
            try:
                if json_res:
                    if 'error' in json_res:
                        if json_res['error'].startswith('error parsing query'):
                            query = params['q']
                            raise exceptions.InfluxDBBadQueryError(query)
                    elif json_res and 'error' in json_res and json_res['error'].endswith('invalid number'):
                        points = kwargs['data']
                        raise exceptions.InfluxDBInvalidNumberError(points)
                elif json_res:
                    if 'error' in json_res and json_res['error'].endswith('bad timestamp'):
                        points = kwargs['data']
                        raise exceptions.InfluxDBInvalidTimestampError(points)
                if res.status_code == 400:
                    raise exceptions.InfluxDBBadRequestError(params)
                if res.status_code == 401:
                    raise exceptions.InfluxDBUnauthorizedError(err)
                raise err
            finally:
                err = None
                del err

        return res

    return func_wrapper