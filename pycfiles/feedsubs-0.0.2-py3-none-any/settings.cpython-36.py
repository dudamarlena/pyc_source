# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/um/settings.py
# Compiled at: 2018-02-05 15:29:56
# Size of source mod 2**32: 191 bytes
from datetime import timedelta
from django.conf import settings
UM_DELETE_ACCOUNT_AFTER = getattr(settings, 'UM_DELETE_ACCOUNT_AFTER', timedelta(days=2))