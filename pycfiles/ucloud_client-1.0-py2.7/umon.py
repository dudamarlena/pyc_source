# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/api/umon.py
# Compiled at: 2015-04-17 09:53:50
from ucloudclient.utils import base

class UnetManager(base.Manager):
    """
    monitor manager class
    """

    def metric_get(self, region, metric_names, resourceid, resource_type, time_range=None, begin_time=None, end_time=None):
        """
        get metric
        :param region:
        :param metric_names:[]
        :param resourceid:
        :param resource_type:
        :param time_range:
        :param begin_time:
        :param end_time:
        :return:
        """
        body = {}
        body['Region'] = region
        body['Action'] = 'GetMetric'
        body['ResourceId'] = resourceid
        body['ResourceType'] = resource_type
        if metric_names:
            for i in range(len(metric_names)):
                body['MetricName.' + str(i)] = metric_names[i]

        if time_range:
            body['TimeRange'] = time_range
        if begin_time:
            body['BeginTime'] = begin_time
        if end_time:
            body['EndTime'] = end_time
        return self._get(body)