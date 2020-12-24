# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/aws_logs_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3872 bytes
"""
This module contains a hook (AwsLogsHook) with some very basic
functionality for interacting with AWS CloudWatch.
"""
from airflow.contrib.hooks.aws_hook import AwsHook

class AwsLogsHook(AwsHook):
    __doc__ = '\n    Interact with AWS CloudWatch Logs\n\n    :param region_name: AWS Region Name (example: us-west-2)\n    :type region_name: str\n    '

    def __init__(self, region_name=None, *args, **kwargs):
        self.region_name = region_name
        (super(AwsLogsHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        """
        Establish an AWS connection for retrieving logs.

        :rtype: CloudWatchLogs.Client
        """
        return self.get_client_type('logs', region_name=(self.region_name))

    def get_log_events(self, log_group, log_stream_name, start_time=0, skip=0, start_from_head=True):
        """
        A generator for log items in a single stream. This will yield all the
        items that are available at the current moment.

        :param log_group: The name of the log group.
        :type log_group: str
        :param log_stream_name: The name of the specific stream.
        :type log_stream_name: str
        :param start_time: The time stamp value to start reading the logs from (default: 0).
        :type start_time: int
        :param skip: The number of log entries to skip at the start (default: 0).
            This is for when there are multiple entries at the same timestamp.
        :type skip: int
        :param start_from_head: whether to start from the beginning (True) of the log or
            at the end of the log (False).
        :type start_from_head: bool
        :rtype: dict
        :return: | A CloudWatch log event with the following key-value pairs:
                 |   'timestamp' (int): The time in milliseconds of the event.
                 |   'message' (str): The log event data.
                 |   'ingestionTime' (int): The time in milliseconds the event was ingested.
        """
        next_token = None
        event_count = 1
        while event_count > 0:
            if next_token is not None:
                token_arg = {'nextToken': next_token}
            else:
                token_arg = {}
            response = (self.get_conn().get_log_events)(logGroupName=log_group, logStreamName=log_stream_name, 
             startTime=start_time, 
             startFromHead=start_from_head, **token_arg)
            events = response['events']
            event_count = len(events)
            if event_count > skip:
                events = events[skip:]
                skip = 0
            else:
                skip = skip - event_count
                events = []
            for ev in events:
                yield ev

            if 'nextForwardToken' in response:
                next_token = response['nextForwardToken']
            else:
                return