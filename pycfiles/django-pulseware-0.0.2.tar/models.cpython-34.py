# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/sf3/lib/python3.4/site-packages/pulseware/models.py
# Compiled at: 2016-01-18 12:22:54
# Size of source mod 2**32: 380 bytes
import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Heartbeat(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'updated at: {}'.format(self.updated_at)