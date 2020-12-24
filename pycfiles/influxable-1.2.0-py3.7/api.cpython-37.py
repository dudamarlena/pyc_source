# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/influxable/api.py
# Compiled at: 2019-10-23 08:36:50
# Size of source mod 2**32: 1654 bytes


class InfluxDBApi:

    @staticmethod
    def get_debug_requests(request, seconds=10):
        url = '/debug/requests'
        seconds = seconds if isinstance(seconds, int) else 10
        params = {'seconds': seconds}
        res = request.get(url=url, params=params)
        return res.json()

    @staticmethod
    def get_debug_vars(request):
        url = '/debug/vars'
        res = request.get(url=url)
        return res.json()

    @staticmethod
    def ping(request, verbose=False):
        url = '/ping'
        verbose = verbose if isinstance(verbose, bool) else False
        params = {'verbose': verbose} if verbose else {}
        res = request.get(url=url, params=params)
        return res.text or True

    @staticmethod
    def execute_query(request, query, method='get', chunked=False, epoch='ns', pretty=False):
        url = '/query'
        params = {'db':request.database_name, 
         'q':query, 
         'epoch':epoch, 
         'chunked':chunked, 
         'pretty':pretty}
        res = request.request(method, url, params=params)
        return res.json()

    @staticmethod
    def write_points(request, points, precision='ns', consistency='all', retention_policy_name='DEFAULT'):
        url = '/write'
        params = {'db':request.database_name, 
         'precision':precision, 
         'consistency':consistency, 
         'retention_policy_name':retention_policy_name}
        request.post(url, params=params, data=points)
        return True