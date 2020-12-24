# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_pushes_light/gateways/onesignal/errors.py
# Compiled at: 2017-11-07 14:45:10
# Size of source mod 2**32: 197 bytes
from django.utils.translation import ugettext as _
BASE_ERROR_CODE = 57664
INVALID_NOTIFICATION_STATUS_CODE = {'code': BASE_ERROR_CODE | 1, 'message': _('Invalid notification status code')}