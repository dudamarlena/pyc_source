# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-groups/vkontakte_groups/mixins.py
# Compiled at: 2015-11-01 17:29:28
from django.conf import settings
from django.db import models
from django.utils import timezone
from m2m_history.fields import ManyToManyHistoryField
from vkontakte_api.decorators import atomic
from vkontakte_api.utils import get_improperly_configured_field

class UserableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'vkontakte_users' in settings.INSTALLED_APPS:
        from vkontakte_users.models import User
        members = ManyToManyHistoryField(User, related_name='members_%(class)ss', versions=True)

        @atomic
        def update_members(self, *args, **kwargs):
            ids = self.__class__.remote.get_members_ids(group=self, *args, **kwargs)
            count = len(ids)
            initial = self.members.versions.count() == 0
            self.members = ids
            if self.members_count != count:
                self.members_count = count
                self.save()
            if initial:
                self.members.get_query_set_through().update(time_from=None)
                self.members.versions.update(added_count=0)
            return self.members

    else:
        members = get_improperly_configured_field('vkontakte_users', True)
        update_members = get_improperly_configured_field('vkontakte_users')


class PhotableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'vkontakte_photos' in settings.INSTALLED_APPS:
        photoalbums = get_improperly_configured_field('vkontakte_photos', True)

        def photos(self):
            from vkontakte_photos.models import Photo
            return Photo.objects.filter(remote_id__startswith='-%s_' % self.remote_id)

        def fetch_photoalbums(self, *args, **kwargs):
            from vkontakte_photos.models import Album
            return Album.remote.fetch(group=self, *args, **kwargs)

    else:
        photoalbums = get_improperly_configured_field('vkontakte_photos', True)
        photos = get_improperly_configured_field('vkontakte_photos', True)
        fetch_photoalbums = get_improperly_configured_field('vkontakte_photos')


class VideoableModelMixin(models.Model):

    class Meta:
        abstract = True

    if 'vkontakte_video' in settings.INSTALLED_APPS:
        videoalbums = get_improperly_configured_field('vkontakte_video', True)
        videos = get_improperly_configured_field('vkontakte_video', True)

        def fetch_videoalbums(self, *args, **kwargs):
            from vkontakte_video.models import Album
            return Album.remote.fetch(owner=self, *args, **kwargs)

        def fetch_videos(self, *args, **kwargs):
            from vkontakte_video.models import Video
            return Video.remote.fetch(owner=self, *args, **kwargs)

    else:
        videoalbums = get_improperly_configured_field('vkontakte_video', True)
        videos = get_improperly_configured_field('vkontakte_video', True)
        fetch_videoalbums = get_improperly_configured_field('vkontakte_video')


class ParseGroupsMixin(object):
    """
    Manager mixin for parsing response with extra cache 'groups'. Used in vkontakte_wall applications
    """

    def parse_response_groups(self, response_list):
        from .models import Group
        users = Group.remote.parse_response_list(response_list.get('groups', []), {'fetched': timezone.now()})
        instances = []
        for instance in users:
            instances += [Group.remote.get_or_create_from_instance(instance)]

        return instances