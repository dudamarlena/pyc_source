# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_organization/handlers.py
# Compiled at: 2016-09-25 10:50:25
from __future__ import unicode_literals
from nodeconductor.structure.log import event_logger

def log_organization_user_save(sender, instance, created=False, **kwargs):
    if created:
        event_logger.user_organization.info(b'User {affected_user_username} has claimed organization {affected_organization}.', event_type=b'user_organization_claimed', event_context={b'affected_user': instance.user, 
           b'affected_organization': instance.organization.abbreviation})
    else:
        previously_approved = instance.tracker.previous(b'is_approved')
        currently_approved = instance.is_approved
        if not previously_approved and currently_approved:
            event_logger.user_organization.info(b'User {affected_user_username} has been approved for organization {affected_organization}.', event_type=b'user_organization_approved', event_context={b'affected_user': instance.user, 
               b'affected_organization': instance.organization.abbreviation})
        elif previously_approved and not currently_approved:
            event_logger.user_organization.info(b'User {affected_user_username} claim for organization {affected_organization} has been rejected.', event_type=b'user_organization_rejected', event_context={b'affected_user': instance.user, 
               b'affected_organization': instance.organization.abbreviation})


def log_organization_user_delete(sender, instance, **kwargs):
    event_logger.user_organization.info(b'User {affected_user_username} has been removed from organization {affected_organization}.', event_type=b'user_organization_removed', event_context={b'affected_user': instance.user, 
       b'affected_organization': instance.organization.abbreviation})