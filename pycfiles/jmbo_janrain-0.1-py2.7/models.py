# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/janrain/models.py
# Compiled at: 2013-06-20 04:08:17
from datetime import datetime
import requests
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.conf import settings
from foundry.models import Member
try:
    import simplejson as json
except ImportError:
    import json

try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

JANRAIN_URL = settings.JANRAIN_URL
STATUS_SYNCED = 1
STATUS_DIRTY = 2
STATUS_CONFLICT = 4
base_payload = {'client_id': settings.JANRAIN_CLIENT_ID, 'client_secret': settings.JANRAIN_CLIENT_SECRET, 
   'type_name': 'user'}
field_mappings = (
 ('first_name', 'givenName'),
 ('last_name', 'familyName'),
 ('email', 'email'),
 ('username', 'displayName'))

def map_user_to_janrain(user):
    """
    Given a user object, provide a dictionary of mapped fields and values to
    give to Janrain to update the user.
    """
    maps = {x[0]:x[1] for x in field_mappings}
    attributes = {}
    user_fields = ('first_name', 'last_name', 'username', 'email')
    for field in user_fields:
        value = getattr(user, field, None)
        if value:
            attributes[maps[field]] = value

    return attributes


@receiver(user_logged_in)
def on_user_logged_in(sender, **kwargs):
    """
    Receiver for when the user logs in. It's placed here on recommendation of
    the Django docs.
    """
    print 'user logged in'
    user = kwargs['user']
    janrain_profile, created = JanrainProfile.objects.get_or_create(user=user)
    if not janrain_profile:
        janrain_profile = JanrainProfile(user=user)
    payload = base_payload.copy()
    if janrain_profile.janrain_uuid:
        pass
    else:
        user_attributes = map_user_to_janrain(user)
        payload['attributes'] = json.dumps(user_attributes)
        response = requests.post('%s/entity.create' % JANRAIN_URL, data=payload)
        struct = json.loads(response.content)
        if struct['stat'] == 'ok':
            janrain_profile.janrain_uuid = struct['uuid']
    janrain_profile.save()


@receiver(post_save, sender=Member)
def on_user_profile_saved(sender, **kwargs):
    """
    Receiver for when the user profile is saved. Push to Janrain.
    """
    janrain_profiles = JanrainProfile.objects.filter(user=kwargs['instance'])
    if len(janrain_profiles) == 0:
        print 'Initial profile save'
        return
    janrain_profile = janrain_profiles[0]
    if janrain_profile.status == STATUS_DIRTY:
        payload = base_payload.copy()
        payload['uuid'] = janrain_profile.janrain_uuid
        user_attributes = map_user_to_janrain(janrain_profile.user)
        payload['value'] = json.dumps(user_attributes)
        response = requests.post('%s/entity.update' % JANRAIN_URL, data=payload)
        struct = json.loads(response.content)
        if struct['stat'] == 'ok':
            janrain_profile.status = STATUS_SYNCED
            janrain_profile.last_synced = datetime.now()
            janrain_profile.save()


class JanrainProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    janrain_uuid = models.CharField(max_length=128, blank=True, null=True)
    last_synced = models.DateTimeField(auto_now_add=True, null=True)
    status = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.user.username