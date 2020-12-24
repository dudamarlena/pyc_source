# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/notifications/api/serializers.py
# Compiled at: 2020-01-31 08:32:40
# Size of source mod 2**32: 1006 bytes
from rest_framework import serializers
from notifications.models import Notification, UserNotification
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class NotificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Notification
        fields = ('name', 'message', 'snooze_time', 'snooze_lock', 'look', 'image')


class UserNotificationSerializer(serializers.HyperlinkedModelSerializer):
    notification = NotificationSerializer()
    user = UserSerializer()

    class Meta:
        model = UserNotification
        fields = ('id', 'notification', 'user', 'seen', 'answer')


class UserNotificationPutSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = UserNotification
        fields = ('answer', 'answer_string')