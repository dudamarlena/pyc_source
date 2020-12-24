# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/hardware/models/device_to_model_rel.py
# Compiled at: 2013-09-27 16:54:33
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.networking.net.models import Device
from . import DeviceModel, Antenna, AntennaModel

class DeviceToModelRel(models.Model):
    """ OneToOne relationship between net.Device and hardware.DeviceModel """
    device = models.OneToOneField(Device, verbose_name=_('device'), related_name='hardware')
    model = models.ForeignKey(DeviceModel)
    cpu = models.CharField(_('CPU'), max_length=255, blank=True)
    ram = models.IntegerField(_('RAM'), blank=True, help_text=_('bytes'))

    class Meta:
        app_label = 'hardware'
        db_table = 'hardware_device_to_model'
        verbose_name = _('Device Model Information')
        verbose_name_plural = _('Device Model Information')

    def __unicode__(self):
        return '%s (%s)' % (self.device.name, self.model.name)

    def save(self, *args, **kwargs):
        """ when creating a new record fill CPU and RAM info if available """
        adding_new = False
        if not self.pk or not self.cpu and not self.ram:
            if self.model.cpu:
                self.cpu = self.model.cpu
            if self.model.ram:
                self.ram = self.model.ram
            adding_new = True
        super(DeviceToModelRel, self).save(*args, **kwargs)
        try:
            antenna_model = self.model.antennamodel
        except AntennaModel.DoesNotExist:
            antenna_model = False

        if adding_new and antenna_model:
            antenna = Antenna(device=self.device, model=self.model.antennamodel)
            wireless_interfaces = self.device.interface_set.filter(type=2)
            if len(wireless_interfaces) > 0:
                antenna.radio = wireless_interfaces[0]
            antenna.save()