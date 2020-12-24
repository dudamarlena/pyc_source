# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/models/district.py
# Compiled at: 2017-01-04 15:00:20
# Size of source mod 2**32: 751 bytes
from django.utils.translation import ugettext as _
from .base import models
from .base import AbstractCity

class District(AbstractCity):
    __doc__ = '\n    Continent Model Class.\n    '
    city = models.ForeignKey('City', verbose_name=_('LOCATION.DISTRICT'), related_name='%(app_label)s_%(class)s_city', null=True, blank=True)

    class Meta:
        app_label = 'geoware'
        db_table = '{app}-{type}'.format(app=app_label, type='district')
        verbose_name = _('LOCATION.DISTRICT')
        verbose_name_plural = _('LOCATION.DISTRICT#plural')
        unique_together = [('name', 'city')]

    @property
    def parent(self):
        if self.city:
            return self.city