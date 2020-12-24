# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/logs/fetcher.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 5505 bytes
"""
Filters & fetches logs from CloudWatch Logs
"""
import time, logging
from samcli.lib.utils.time import to_timestamp, to_datetime
from .event import LogEvent
LOG = logging.getLogger(__name__)

class LogsFetcher:
    __doc__ = '\n    Fetch logs from a CloudWatch Logs group with the ability to scope to a particular time, filter by\n    a pattern, and in the future possibly multiplex from from multiple streams together.\n    '

    def __init__(self, cw_client=None):
        """
        Initialize the fetcher

        Parameters
        ----------
        cw_client
            CloudWatch Logs Client from AWS SDK
        """
        self.cw_client = cw_client

    def fetch(self, log_group_name, start=None, end=None, filter_pattern=None):
        """
        Fetch logs from all streams under the given CloudWatch Log Group and yields in the output. Optionally, caller
        can filter the logs using a pattern or a start/end time.

        Parameters
        ----------
        log_group_name : string
            Name of CloudWatch Logs Group to query.

        start : datetime.datetime
            Optional start time for logs.

        end : datetime.datetime
            Optional end time for logs.

        filter_pattern : str
            Expression to filter the logs by. This is passed directly to CloudWatch, so any expression supported by
            CloudWatch Logs API is supported here.

        Yields
        ------

        samcli.lib.logs.event.LogEvent
            Object containing the information from each log event returned by CloudWatch Logs
        """
        kwargs = {'logGroupName':log_group_name, 
         'interleaved':True}
        if start:
            kwargs['startTime'] = to_timestamp(start)
        if end:
            kwargs['endTime'] = to_timestamp(end)
        if filter_pattern:
            kwargs['filterPattern'] = filter_pattern
        while 1:
            LOG.debug('Fetching logs from CloudWatch with parameters %s', kwargs)
            result = (self.cw_client.filter_log_events)(**kwargs)
            for event in result.get('events', []):
                yield LogEvent(log_group_name, event)

            next_token = result.get('nextToken', None)
            kwargs['nextToken'] = next_token
            if not next_token:
                break

    def tail(self, log_group_name, start=None, filter_pattern=None, max_retries=1000, poll_interval=0.3):
        """
        ** This is a long blocking call **

        Fetches logs from CloudWatch logs similar to the ``fetch`` method, but instead of stopping after all logs have
        been fetched, this method continues to poll CloudWatch for new logs. So this essentially simulates the
        ``tail -f`` bash command.

        If no logs are available, then it keep polling for ``timeout`` number of seconds before exiting. This method
        polls CloudWatch at around ~3 Calls Per Second to stay below the 5TPS limit.

        Parameters
        ----------
        log_group_name : str
            Name of CloudWatch Logs Group to query.

        start : datetime.datetime
            Optional start time for logs. Defaults to '5m ago'

        filter_pattern : str
            Expression to filter the logs by. This is passed directly to CloudWatch, so any expression supported by
            CloudWatch Logs API is supported here.

        max_retries : int
            When logs are not available, this value determines the number of times to retry fetching logs before giving
            up. This counter is reset every time new logs are available.

        poll_interval : float
            Number of fractional seconds wait before polling again. Defaults to 300milliseconds.
            If no new logs available, this method will stop polling after ``max_retries * poll_interval`` seconds

        Yields
        ------
        samcli.lib.logs.event.LogEvent
            Object containing the information from each log event returned by CloudWatch Logs
        """
        latest_event_time = 0
        if start:
            latest_event_time = to_timestamp(start)
        counter = max_retries
        while counter > 0:
            LOG.debug('Tailing logs from %s starting at %s', log_group_name, str(latest_event_time))
            has_data = False
            counter -= 1
            events_itr = self.fetch(log_group_name, start=(to_datetime(latest_event_time)), filter_pattern=filter_pattern)
            for event in events_itr:
                has_data = True
                if event.timestamp_millis > latest_event_time:
                    latest_event_time = event.timestamp_millis
                yield event

            if has_data:
                counter = max_retries
                latest_event_time += 1
            time.sleep(poll_interval)