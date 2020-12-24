# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/filter_notification.py
# Compiled at: 2019-02-28 08:22:31
# Size of source mod 2**32: 1209 bytes
from .notification import Notification, common_notification_paramenters
from .filter import Filter
from .utils import merge_dicts

class FilterNotification(Notification):
    'Notification based on specific filters\n\n    Attributes:\n        filters\n        {common_notification_paramenters}\n    '.format(common_notification_paramenters=common_notification_paramenters)

    def __init__(self, filters, **kwargs):
        (Notification.__init__)(self, **kwargs)
        self.filters = []
        next_operator = None
        for index, filter in enumerate(filters):
            if isinstance(filter, Filter):
                if not next_operator:
                    self.filters.append(filter.data)
                else:
                    self.filters.append(merge_dicts(filter.data, {'operator': next_operator}))
                    next_operator = None

    def get_data(self):
        return merge_dicts(self.get_common_data(), {'filters': self.filters})