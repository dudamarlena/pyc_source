# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-groups/odnoklassniki_groups/models.py
# Compiled at: 2015-03-21 09:13:41
import logging
from django.conf import settings
from django.contrib.contenttypes import generic
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext as _
from odnoklassniki_api.decorators import atomic, fetch_all, opt_generator
from odnoklassniki_api.fields import JSONField
from odnoklassniki_api.models import OdnoklassnikiManager, OdnoklassnikiPKModel
from .mixins import DiscussionsModelMixin, PhotosModelMixin, UsersModelMixin
log = logging.getLogger('odnoklassniki_groups')

class GroupRemoteManager(OdnoklassnikiManager):

    @atomic
    def fetch(self, ids, **kwargs):
        kwargs['uids'] = (',').join(map(lambda i: str(i), ids))
        kwargs['fields'] = self.get_request_fields('group')
        return super(GroupRemoteManager, self).fetch(**kwargs)

    @fetch_all(always_all=True)
    def get_members_ids(self, group, count=1000, **kwargs):
        kwargs['uid'] = group.pk
        kwargs['count'] = count
        response = self.api_call('get_members', **kwargs)
        ids = [ m['userId'] for m in response['members'] ]
        return (ids, response)


class Group(DiscussionsModelMixin, PhotosModelMixin, UsersModelMixin, OdnoklassnikiPKModel):

    class Meta:
        verbose_name = _('Odnoklassniki group')
        verbose_name_plural = _('Odnoklassniki groups')

    resolve_screen_name_type = 'GROUP'
    methods_namespace = 'group'
    remote_pk_field = 'uid'
    slug_prefix = 'group'
    name = models.CharField(max_length=800)
    description = models.TextField()
    shortname = models.CharField(max_length=50)
    members_count = models.PositiveIntegerField(null=True)
    photo_id = models.BigIntegerField(null=True)
    pic128x128 = models.URLField()
    pic50x50 = models.URLField()
    pic640x480 = models.URLField()
    premium = models.NullBooleanField()
    private = models.NullBooleanField()
    shop_visible_admin = models.NullBooleanField()
    shop_visible_public = models.NullBooleanField()
    attrs = JSONField(null=True)
    remote = GroupRemoteManager(methods={'get': 'getInfo', 
       'get_members': 'getMembers'})

    def __unicode__(self):
        return self.name

    @property
    def refresh_kwargs(self):
        return {'ids': [self.pk]}

    def parse(self, response):
        if 'main_photo' in response:
            response['main_photo'].pop('id', None)
            response.update(response.pop('main_photo'))
        if 'picAvatar' in response:
            response['pic50x50'] = response.pop('picAvatar')
        super(Group, self).parse(response)
        return


from . import signals