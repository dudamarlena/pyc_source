# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egonzalez/EricssonGitLab/clients/mediafirst-analytics-backend/ivibackend/monitoring/statsd.py
# Compiled at: 2018-06-14 03:49:25
# Size of source mod 2**32: 617 bytes
from datadog import DogStatsd

class StatsD:

    class __StatsD:

        def __init__(self, host, port, namespace):
            self.client = DogStatsd(host=host, port=port, namespace=namespace)

        def __str__(self):
            return repr(self) + self.client

    instance = None

    def __init__(self, host, port, namespace):
        if not StatsD.instance:
            StatsD.instance = StatsD._StatsD__StatsD(host, port, namespace)
        else:
            StatsD.instance.client = DogStatsd(host=host, port=port, namespace=namespace)

    def __getattr__(self, name):
        return getattr(self.instance, name)