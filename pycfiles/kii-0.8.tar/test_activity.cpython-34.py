# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/activity/tests/test_activity.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 538 bytes
from kii.stream.tests import base
from kii.stream import models as stream_models

class NotificationTestCase(base.StreamTestCase):

    def test_notification_is_created_for_each_following_user(self):
        stream = stream_models.Stream.objects.get_user_stream(self.users[0])
        si = self.G(stream_models.StreamItem, root=stream)
        c = self.G(stream_models.ItemComment, subject=si, user=self.users[1])
        self.assertEqual(self.users[0].notifications.all().first().action.action_object, c)