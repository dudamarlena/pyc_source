# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/useravatar.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import models
from sentry.db.models import BaseManager, FlexibleForeignKey
from . import AvatarBase

class UserAvatar(AvatarBase):
    """
    A UserAvatar associates a User with their avatar photo File
    and contains their preferences for avatar type.
    """
    AVATAR_TYPES = (
     (0, 'letter_avatar'), (1, 'upload'), (2, 'gravatar'))
    FILE_TYPE = 'avatar.file'
    user = FlexibleForeignKey('sentry.User', unique=True, related_name='avatar')
    avatar_type = models.PositiveSmallIntegerField(default=0, choices=AVATAR_TYPES)
    objects = BaseManager(cache_fields=['user'])

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_useravatar'

    def get_cache_key(self, size):
        return 'avatar:%s:%s' % (self.user_id, size)