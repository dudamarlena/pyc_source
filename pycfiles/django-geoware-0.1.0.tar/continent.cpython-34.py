# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/models/continent.py
# Compiled at: 2017-01-27 10:18:13
# Size of source mod 2**32: 734 bytes
from django.utils.translation import ugettext as _
from .base import models
from .base import AbstractLocation

class Continent(AbstractLocation):
    __doc__ = '\n    Continent Model Class.\n    '
    code = models.CharField(_('Code'), db_index=True, max_length=2)
    iso_n = models.CharField('M49', db_index=True, max_length=3, null=True, blank=True)

    class Meta:
        app_label = 'geoware'
        db_table = '{app}-{type}'.format(app=app_label, type='continent')
        verbose_name = _('Continent')
        verbose_name_plural = _('Continents')
        unique_together = [('name', 'code')]

    @property
    def parent(self):
        pass