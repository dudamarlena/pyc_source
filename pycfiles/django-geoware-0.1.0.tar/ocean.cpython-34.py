# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/models/ocean.py
# Compiled at: 2017-01-27 10:25:36
# Size of source mod 2**32: 709 bytes
from django.utils.translation import ugettext as _
from .base import models
from .base import AbstractLocation

class Ocean(AbstractLocation):
    __doc__ = '\n    Ocean Model Class.\n    '
    depth = models.PositiveIntegerField(_('Depth'), null=True, blank=True)
    depth_name = models.CharField(_('Depth Name'), max_length=254, null=True, blank=True)

    class Meta:
        app_label = 'geoware'
        db_table = '{app}-{type}'.format(app=app_label, type='ocean')
        verbose_name = _('Ocean')
        verbose_name_plural = _('Oceans')
        unique_together = ('name', )

    @property
    def parent(self):
        pass