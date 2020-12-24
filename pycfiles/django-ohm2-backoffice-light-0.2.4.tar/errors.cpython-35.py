# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_backoffice_light/api/v1/errors.py
# Compiled at: 2017-12-28 21:01:47
# Size of source mod 2**32: 173 bytes
from django.utils.translation import ugettext as _
BASE_ERROR_CODE = 163648
BOTH_CANT_BE_EMPTY = {'code': BASE_ERROR_CODE | 1, 
 'message': _("Both can't be empty")}