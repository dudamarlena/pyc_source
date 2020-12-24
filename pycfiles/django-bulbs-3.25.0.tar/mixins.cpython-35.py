# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/videos/mixins.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 312 bytes
from django.db import models
from .models import VideohubVideo

class VideoMixin(models.Model):
    __doc__ = 'Provides an OnionStudios (videohub) reference ID, standardized across all properties.'
    videohub_ref = models.ForeignKey(VideohubVideo, null=True, blank=True)

    class Meta:
        abstract = True