# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/signals.py
# Compiled at: 2019-05-14 12:25:52
# Size of source mod 2**32: 1078 bytes
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Ticket
import logging
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Ticket)
def handle_ticket_sla_update_pre_save(sender, instance, **kwargs):
    try:
        old_ticket = Ticket.objects.get(id=(instance.id))
        if not getattr(old_ticket.status, 'escalation_status', None) or not getattr(instance.status, 'escalation_status', None):
            return
        if old_ticket.status > instance.status or old_ticket.status < instance.status:
            instance.calculate_sla_expiry()
        else:
            if old_ticket.priority != instance.priority:
                instance.calculate_sla_expiry()
    except Ticket.DoesNotExist:
        instance.calculate_sla_expiry()