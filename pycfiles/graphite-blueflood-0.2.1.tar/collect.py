# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shin4590/src/forks/blueflood-carbon-forwarder/bluefloodserver/collect.py
# Compiled at: 2016-01-20 11:36:19
import logging
from blueflood import LimitExceededException
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.python import log

class IFlush:

    def flush(self, metrics):
        raise 'Not Implemented'


class ConsumeFlush(IFlush):

    def flush(self, metrics):
        pass


class FileFlush(IFlush):

    def __init__(self, filename):
        self.filename = filename

    def flush(self, metrics):
        with open(self.filename, 'a') as (outfile):
            for name, time, value in metrics:
                outfile.write(('{} {} {}\n').format(name, time, value))


class BluefloodFlush(IFlush):

    def __init__(self, client, ttl=86400, metric_prefix=None):
        self.client = client
        self.ttl = ttl
        self.metric_prefix = metric_prefix
        log.msg(('Prepending all metrics with custom string {}').format(metric_prefix), level=logging.DEBUG)

    @inlineCallbacks
    def flush(self, metrics):
        for name, time, value in metrics:
            if self.metric_prefix:
                metric_name = self.metric_prefix + '.' + name
            else:
                metric_name = name
            try:
                self.client.ingest(metric_name, time, value, self.ttl)
            except LimitExceededException:
                yield self.client.commit()
                self.client.ingest(metric_name, time, value, self.ttl)

        yield self.client.commit()
        returnValue(None)
        return


class MetricCollection:

    def __init__(self, flusher):
        self._metrics = []
        self.flusher = flusher

    def collect(self, metric, datapoint):
        self._metrics.append((metric, datapoint[0], datapoint[1]))

    def flush(self):
        if self._metrics:
            self.flusher.flush(self._metrics)
            self._metrics = []

    def count(self):
        return len(self._metrics)