# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_pushes_light/gateways/onesignal/models.py
# Compiled at: 2018-09-28 10:18:25
# Size of source mod 2**32: 772 bytes
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext as _
from ohm2_handlers_light.models import BaseModel
from ohm2_pushes_light import models as ohm2_pushes_light_models
from . import managers
from . import settings

class Device(ohm2_pushes_light_models.Device):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='onesignal_device')
    player_id = models.CharField(max_length=settings.STRING_DOUBLE)
    push_token = models.CharField(max_length=settings.STRING_DOUBLE)

    def __str__(self):
        return '[%s][%s][player id: %s]' % (self.user.get_username(), self.platform_str, self.player_id)