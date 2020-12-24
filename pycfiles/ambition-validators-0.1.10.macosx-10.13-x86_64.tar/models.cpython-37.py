# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/ambition_validators/models.py
# Compiled at: 2018-01-29 14:27:09
# Size of source mod 2**32: 111 bytes
from django.conf import settings
if settings.APP_NAME == 'ambition_validators':
    from .tests import models