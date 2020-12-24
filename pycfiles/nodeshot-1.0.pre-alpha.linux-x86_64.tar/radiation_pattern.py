# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/hardware/models/radiation_pattern.py
# Compiled at: 2014-05-08 09:18:56
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate
from . import ImageMixin, AntennaModel

class RadiationPattern(BaseDate, ImageMixin):
    """ Radiation Pattern of an Antenna Model """
    antenna_model = models.ForeignKey(AntennaModel)
    type = models.CharField(_('type'), max_length=30)
    image = models.ImageField(upload_to='antennas/radiation_patterns/', verbose_name=_('image'))

    def __unicode__(self):
        return _('radiation pattern for antenna model: %s' % self.antenna_model)

    class Meta:
        app_label = 'hardware'
        db_table = 'hardware_radiation_pattern'