# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/segment_notification.py
# Compiled at: 2019-03-19 08:10:19
# Size of source mod 2**32: 1005 bytes
from itertools import chain
from .notification import Notification, common_notification_paramenters

class SegmentNotification(Notification):
    'Notification based on specific filters\n\n    Attributes:\n        included_segment\n        excluded_segments\n        {common_notification_paramenters}\n    '.format(common_notification_paramenters=common_notification_paramenters)
    ALL = 'All'
    ACTIVE_USERS = 'Active Users'
    ENGAGED_USERS = 'Engaged Users'
    INACTIVE_USERS = 'Inactive Users'

    def __init__(self, included_segments=None, excluded_segments=None, **kwargs):
        (Notification.__init__)(self, **kwargs)
        self.included_segments = included_segments
        self.excluded_segments = excluded_segments

    def get_data(self):
        return dict(chain({'included_segments':self.included_segments, 
         'excluded_segments':self.excluded_segments}.items(), self.get_common_data().items()))