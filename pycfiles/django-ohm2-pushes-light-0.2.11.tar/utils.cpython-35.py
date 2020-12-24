# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_pushes_light/gateways/onesignal/utils.py
# Compiled at: 2018-09-28 10:24:42
# Size of source mod 2**32: 3083 bytes
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import models as onesignal_models
from . import errors as onesignal_errors
from . import settings
import simplejson as json, os, time, random, requests
random_string = 'L4grZ9Lzlr7eByGMzCsullCuUkk2b8BO'

def parse_device_attributes(**kwargs):
    attributes = {}
    user = kwargs.get('user', None)
    if user is not None:
        attributes['user'] = user
    platform = kwargs.get('platform', None)
    if platform is not None:
        attributes['platform'] = int(platform)
    player_id = kwargs.get('player_id', None)
    if player_id is not None:
        attributes['player_id'] = player_id.strip()
    push_token = kwargs.get('push_token', None)
    if push_token is not None:
        attributes['push_token'] = push_token.strip()
    return attributes


def create_device(user, platform, player_id, push_token, **kwargs):
    kwargs['user'] = user
    kwargs['gateway'] = onesignal_models.Device.gateway_onesignal[0]
    kwargs['platform'] = platform
    kwargs['player_id'] = player_id
    kwargs['push_token'] = push_token
    for key, value in parse_device_attributes(**kwargs).items():
        kwargs[key] = value

    return h_utils.db_create(onesignal_models.Device, **kwargs)


def get_device(**kwargs):
    return h_utils.db_get(onesignal_models.Device, **kwargs)


def get_or_none_device(**kwargs):
    return h_utils.db_get_or_none(onesignal_models.Device, **kwargs)


def filter_device(**kwargs):
    return h_utils.db_filter(onesignal_models.Device, **kwargs)


def q_device(q):
    return h_utils.db_q(onesignal_models.Device, q)


def update_device(entry, **kwargs):
    attributes = {}
    for key, value in parse_device_attributes(**kwargs).items():
        attributes[key] = value

    return h_utils.db_update(entry, **attributes)


def get_platform_ios():
    return onesignal_models.Device.platform_ios


def get_platform_android():
    return onesignal_models.Device.platform_android


def send_notifications(message, player_ids, **options):
    contents = {'en': message.title}
    payload = {'app_id': settings.APP_ID, 
     'include_player_ids': player_ids, 
     'contents': contents, 
     'data': message.get_onesignal_data()}
    res = requests.post(settings.API_NOTIFICATIONS_URL, headers=settings.HEADERS, data=json.dumps(payload))
    if res.status_code != 200:
        raise RunException(**onesignal_errors.INVALID_NOTIFICATION_STATUS_CODE)
    ret = res.json()
    pushed = True
    return pushed