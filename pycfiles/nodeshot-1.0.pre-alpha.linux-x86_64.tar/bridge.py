# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/net/models/interfaces/bridge.py
# Compiled at: 2013-09-08 06:03:46
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from nodeshot.networking.net.models import Interface
from nodeshot.networking.net.models.choices import INTERFACE_TYPES

class Bridge(Interface):
    """ Bridge interface """
    interfaces = models.ManyToManyField(Interface, verbose_name=_('interfaces'), related_name='bridge_interfaces')
    objects = Interface.objects.__class__()

    class Meta:
        app_label = 'net'
        db_table = 'net_interface_bridge'
        verbose_name = _('bridge interface')
        verbose_name_plural = _('bridge interfaces')

    def save(self, *args, **kwargs):
        """ automatically set Interface.type to bridge """
        self.type = INTERFACE_TYPES.get('bridge')
        super(Bridge, self).save(*args, **kwargs)


from django.dispatch import receiver
from django.db.models.signals import m2m_changed

@receiver(m2m_changed, sender=Bridge.interfaces.through)
def validate_bridged_interfaces(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Bridge interface validation constraints:
        * can't bridge interfaces of different devices
        * can't bridge self
        * there must be at least two interfaces bridged
    """
    if action != 'pre_add':
        return
    interfaces = Interface.objects.filter(pk__in=pk_set)
    device = instance.device
    device_id = instance.device.id
    invalid_interfaces = []
    trying_to_bridge_self = False
    for interface in interfaces:
        if interface.device_id != device_id:
            invalid_interfaces.append(interface.mac)
        elif interface.id == instance.id:
            trying_to_bridge_self = True

    if instance.interfaces.count() < 2 and len(pk_set) < 2:
        raise ValidationError(_('You must bridge at least 2 interfaces'))
    if invalid_interfaces:
        raise ValidationError(_('The interface%s %s %s not belong to device "%s"' % (
         's' if len(invalid_interfaces) > 1 else '',
         (', ').join(invalid_interfaces),
         'do' if len(invalid_interfaces) > 1 else 'does',
         device.name)))
    elif trying_to_bridge_self:
        raise ValidationError(_('Cannot bridge interface %s because that is the actual interface you are editing' % instance.mac))