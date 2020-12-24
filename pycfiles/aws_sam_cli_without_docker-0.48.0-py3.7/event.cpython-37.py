# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/logs/event.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2046 bytes
"""
Represents CloudWatch Log Event
"""
import logging
from samcli.lib.utils.time import timestamp_to_iso
LOG = logging.getLogger(__name__)

class LogEvent:
    __doc__ = '\n    Data object representing a CloudWatch Log Event\n    '
    log_group_name = None
    log_stream_name = None
    timestamp = None
    message = None

    def __init__(self, log_group_name, event_dict):
        """
        Creates instance of the class

        Parameters
        ----------
        event_dict : dict
            Dict of log event data returned by CloudWatch Logs API.
            https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_FilteredLogEvent.html
        """
        self.log_group_name = log_group_name
        if not event_dict:
            return
        self.log_stream_name = event_dict.get('logStreamName')
        self.message = event_dict.get('message', '')
        self.timestamp_millis = event_dict.get('timestamp')
        if self.timestamp_millis:
            self.timestamp = timestamp_to_iso(int(self.timestamp_millis))

    def __eq__(self, other):
        if not isinstance(other, LogEvent):
            return False
        return self.log_group_name == other.log_group_name and self.log_stream_name == other.log_stream_name and self.timestamp == other.timestamp and self.message == other.message

    def __repr__(self):
        return str({'log_group_name':self.log_group_name, 
         'log_stream_name':self.log_stream_name, 
         'message':self.message, 
         'timestamp':self.timestamp})