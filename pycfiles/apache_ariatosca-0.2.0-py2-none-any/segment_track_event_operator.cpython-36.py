# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/segment_track_event_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2752 bytes
from airflow.contrib.hooks.segment_hook import SegmentHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SegmentTrackEventOperator(BaseOperator):
    """SegmentTrackEventOperator"""
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