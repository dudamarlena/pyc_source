# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/doozdev/backend/restful-backend/apps/geoware/models/region.py
# Compiled at: 2017-01-12 19:44:32
# Size of source mod 2**32: 1257 bytes
from django.utils.translation import ugettext as _
from .base import models
from .base import AbstractLocation

class Region(AbstractLocation):
    __doc__ = '\n    Region Model Class.\n    '
    country = models.ForeignKey('Country', verbose_name=_('LOCATION.REGION.COUNTRY'), related_name='%(app_label)s_%(class)s_country', null=True, blank=True)
    capital = models.ForeignKey('City', verbose_name=_('LOCATION.REGION.CAPITAL'), related_name='%(app_label)s_%(class)s_capital', null=True, blank=True)
    code = models.CharField(_('LOCATION.REGION.CODE'), max_length=40, null=True, blank=True)
    fips = models.CharField(_('LOCATION.REGION.CODE_FIPS'), max_length=40, null=True, blank=True)

    class Meta:
        app_label = 'geoware'
        db_table = '{app}-{type}'.format(app=app_label, type='region')
        verbose_name = _('LOCATION.REGION')
        verbose_name_plural = _('LOCATION.REGION#plural')
        unique_together = [('fips', 'name_std', 'country')]

    @property
    def parent(self):
        if self.country:
            return self.country