# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/response.py
# Compiled at: 2019-10-23 08:36:50
# Size of source mod 2**32: 1833 bytes


class InfluxDBResponse:

    def __init__(self, raw_json):
        self._raw_json = raw_json

    @property
    def raw(self):
        return self._raw_json

    @property
    def main_serie(self):
        series = self.series
        if len(series):
            return series[0]

    @property
    def series(self):
        if 'results' in self.raw:
            results = self.raw['results']
            if len(results):
                result = results[0]
                if 'series' in result:
                    return [InfluxDBSerieResponse(s) for s in result['series']]
        return []

    @property
    def error(self):
        main_level_error = self.raw.get('error', None)
        if main_level_error:
            return main_level_error
        if 'results' in self.raw:
            results = self.raw['results']
            if len(results):
                result = results[0]
                if 'error' in result:
                    return result.get('error', None)

    def raise_if_error(self):
        if self.error:
            from .exceptions import InfluxDBError
            raise InfluxDBError(self.error)


class InfluxDBSerieResponse:

    def __init__(self, json_serie):
        self._raw_json_serie = json_serie

    @property
    def raw(self):
        return self._raw_json_serie

    @property
    def columns(self):
        return self._raw_json_serie['columns']

    @property
    def name(self):
        return self._raw_json_serie.get('name', 'default')

    @property
    def values(self):
        return self._raw_json_serie.get('values', None)


class InfluxDBErrorResponse:

    def __init__(self, raw_json):
        self._raw_json = raw_json

    @property
    def raw(self):
        return self._raw_json

    @property
    def error(self):
        return self.raw['error']