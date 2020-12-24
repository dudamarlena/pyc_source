# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/segment_track_event_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2752 bytes
from airflow.contrib.hooks.segment_hook import SegmentHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SegmentTrackEventOperator(BaseOperator):
    __doc__ = "\n    Send Track Event to Segment for a specified user_id and event\n\n    :param user_id: The ID for this user in your database. (templated)\n    :type user_id: str\n    :param event: The name of the event you're tracking. (templated)\n    :type event: str\n    :param properties: A dictionary of properties for the event. (templated)\n    :type properties: dict\n    :param segment_conn_id: The connection ID to use when connecting to Segment.\n    :type segment_conn_id: str\n    :param segment_debug_mode: Determines whether Segment should run in debug mode.\n        Defaults to False\n    :type segment_debug_mode: bool\n    "
    template_fields = ('user_id', 'event', 'properties')
    ui_color = '#ffd700'

    @apply_defaults
    def __init__(self, user_id, event, properties=None, segment_conn_id='segment_default', segment_debug_mode=False, *args, **kwargs):
        (super(SegmentTrackEventOperator, self).__init__)(*args, **kwargs)
        self.user_id = user_id
        self.event = event
        properties = properties or {}
        self.properties = properties
        self.segment_debug_mode = segment_debug_mode
        self.segment_conn_id = segment_conn_id

    def execute(self, context):
        hook = SegmentHook(segment_conn_id=(self.segment_conn_id), segment_debug_mode=(self.segment_debug_mode))
        self.log.info('Sending track event (%s) for user id: %s with properties: %s', self.event, self.user_id, self.properties)
        hook.track(user_id=(self.user_id),
          event=(self.event),
          properties=(self.properties))