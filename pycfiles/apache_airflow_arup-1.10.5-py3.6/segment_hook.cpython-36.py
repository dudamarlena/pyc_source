# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/segment_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 3673 bytes
"""
This module contains a Segment Hook
which allows you to connect to your Segment account,
retrieve data from it or write to that file.

NOTE:   this hook also relies on the Segment analytics package:
        https://github.com/segmentio/analytics-python
"""
import analytics
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException

class SegmentHook(BaseHook):

    def __init__(self, segment_conn_id='segment_default', segment_debug_mode=False, *args, **kwargs):
        """
        Create new connection to Segment
        and allows you to pull data out of Segment or write to it.

        You can then use that file with other
        Airflow operators to move the data around or interact with segment.

        :param segment_conn_id: the name of the connection that has the parameters
                            we need to connect to Segment.
                            The connection should be type `json` and include a
                            write_key security token in the `Extras` field.
        :type segment_conn_id: str
        :param segment_debug_mode: Determines whether Segment should run in debug mode.
        Defaults to False
        :type segment_debug_mode: bool
        .. note::
            You must include a JSON structure in the `Extras` field.
            We need a user's security token to connect to Segment.
            So we define it in the `Extras` field as:
                `{"write_key":"YOUR_SECURITY_TOKEN"}`
        """
        self.segment_conn_id = segment_conn_id
        self.segment_debug_mode = segment_debug_mode
        self._args = args
        self._kwargs = kwargs
        self.connection = self.get_connection(self.segment_conn_id)
        self.extras = self.connection.extra_dejson
        self.write_key = self.extras.get('write_key')
        if self.write_key is None:
            raise AirflowException('No Segment write key provided')

    def get_conn(self):
        self.log.info('Setting write key for Segment analytics connection')
        analytics.debug = self.segment_debug_mode
        if self.segment_debug_mode:
            self.log.info('Setting Segment analytics connection to debug mode')
        analytics.on_error = self.on_error
        analytics.write_key = self.write_key
        return analytics

    def on_error(self, error, items):
        """
        Handles error callbacks when using Segment with segment_debug_mode set to True
        """
        self.log.error('Encountered Segment error: {segment_error} with items: {with_items}'.format(segment_error=error,
          with_items=items))
        raise AirflowException('Segment error: {}'.format(error))