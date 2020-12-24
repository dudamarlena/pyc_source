# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rq_exporter/collector.py
# Compiled at: 2020-04-23 07:03:46
# Size of source mod 2**32: 1570 bytes
"""
RQ metrics collector.

"""
import logging
from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily
from .utils import get_workers_stats, get_jobs_by_queue
logger = logging.getLogger(__name__)

class RQCollector(object):
    __doc__ = 'RQ stats collector.\n\n    Args:\n        connection (redis.Redis): Redis connection instance.\n\n    '

    def __init__(self, connection=None):
        self.connection = connection
        self.summary = Summary('rq_request_processing_seconds', 'Time spent processing RQ stats')

    def collect(self):
        """Collect RQ Metrics.

        Note:
            This method will be called on registration and every time the metrics are requested.

        Yields:
            RQ metrics for workers and jobs.

        """
        logger.debug('Collecting the RQ metrics...')
        with self.summary.time():
            rq_workers = GaugeMetricFamily('rq_workers', 'RQ workers', labels=['name', 'state', 'queues'])
            rq_jobs = GaugeMetricFamily('rq_jobs', 'RQ jobs by state', labels=['queue', 'status'])
            for worker in get_workers_stats(self.connection):
                rq_workers.add_metric([worker['name'], worker['state'], ','.join(worker['queues'])], 1)

            yield rq_workers
            for queue_name, jobs in get_jobs_by_queue(self.connection).items():
                for status, count in jobs.items():
                    rq_jobs.add_metric([queue_name, status], count)

            yield rq_jobs