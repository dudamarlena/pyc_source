# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/saltstack/handlers.py
# Compiled at: 2016-09-28 02:05:53
from __future__ import unicode_literals
import logging
from django.db import models
from .log import event_logger
logger = logging.getLogger(__name__)

def get_property_identifier(instance):
    property_identifier = b'{property_name}'
    if b'email' in instance.get_log_fields():
        property_identifier += b' ({property_email})'
    elif b'username' in instance.get_log_fields():
        property_identifier += b' ({property_username})'
    return property_identifier


def is_field_loggable(instance, field):
    if field in ('admin_id', 'backend_id', 'password'):
        return False
    try:
        if isinstance(instance._meta.get_field(field), models.ForeignKey):
            return False
    except models.fields.FieldDoesNotExist:
        return False

    return True


def log_saltstack_property_created(sender, instance, created=False, **kwargs):
    if created:
        event_logger.saltstack_property.info(b'%s %s has been created in {resource_full_name}.' % (
         instance.get_type_display_name(), get_property_identifier(instance)), event_type=b'saltstack_property_creation_succeeded', event_context={b'property': instance})
    else:
        changes = []
        for field in instance.tracker.changed():
            if not is_field_loggable(instance, field):
                continue
            changes.append(b'%s "%s" has been changed to "%s"' % (
             field, instance.tracker.previous(field), getattr(instance, field)))

        if not changes:
            return
        event_logger.saltstack_property.info(b'%s %s has been updated in {resource_full_name}. Changes: %s.' % (
         instance.get_type_display_name(), get_property_identifier(instance), (b', ').join(changes)), event_type=b'saltstack_property_update_succeeded', event_context={b'property': instance})


def log_saltstack_property_deleted(sender, instance, **kwargs):
    event_logger.saltstack_property.info(b'%s %s has been deleted from {resource_full_name}.' % (
     instance.get_type_display_name(), get_property_identifier(instance)), event_type=b'saltstack_property_deletion_succeeded', event_context={b'property': instance})