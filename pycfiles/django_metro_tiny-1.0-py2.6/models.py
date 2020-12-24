# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/metro_tiny/models.py
# Compiled at: 2012-03-18 16:28:04
from django.utils.translation import ugettext_lazy as _
from django.db import models
from cities_tiny.models import City

class MetroLine(models.Model):
    name = models.CharField(verbose_name=_('line name'), max_length=200)
    city = models.ForeignKey(City, verbose_name=_('city'))

    class Meta:
        verbose_name = _('Metro line')
        verbose_name_plural = _('Metro lines')
        unique_together = (('city', 'name'), )
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class MetroStation(models.Model):
    name = models.CharField(verbose_name=_('station name'), max_length=200)
    line = models.ForeignKey(MetroLine, verbose_name=_('line'))

    class Meta:
        verbose_name = _('Metro station')
        verbose_name_plural = _('Metro stations')
        unique_together = (('line', 'name'), )
        ordering = ('name', )

    def __unicode__(self):
        if MetroStation.objects.filter(line__city=self.line.city, name=self.name).count() > 1:
            return '%s (%s)' % (self.name, self.line)
        return self.name