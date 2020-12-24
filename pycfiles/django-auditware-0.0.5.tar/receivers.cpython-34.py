# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/sf3/apps/django-auditware/auditware/receivers.py
# Compiled at: 2016-04-05 16:17:06
# Size of source mod 2**32: 2198 bytes
import logging
from django.contrib.auth import signals as django_signals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ipware.ip import get_ip
from .models import UserAudit
from . import utils as util
from . import defaults as defs
log = logging.getLogger('auditware.listeners')

def truncate_to_fit(text, len):
    """
    Truncate text to specified length.
    """
    return text[:len]


def user_audit_create(sender, user, request, **kwargs):
    """ Create a user activity audit when user is logged in """
    audit_key = util.get_audit_key(request.session.session_key)
    try:
        uaa = UserAudit.objects.get(audit_key=audit_key)
    except UserAudit.DoesNotExist:
        data = {'user': user, 
         'audit_key': audit_key, 
         'user_agent': truncate_to_fit(request.META.get('HTTP_USER_AGENT', 'Unknown'), 255), 
         'ip_address': get_ip(request), 
         'referrer': truncate_to_fit(request.META.get('HTTP_REFERER', 'Unknown'), 255), 
         'last_page': truncate_to_fit(request.path or '/', 255)}
        uaa = UserAudit(**data)

    log.info(_('User {0} logged in'.format(user.email)))
    uaa.save()
    request.session[defs.AUDITWARE_SESSION_KEY] = audit_key
    request.session.modified = True
    util.cleanup_user_audits(user)


def user_audit_delete(sender, user, request, **kwargs):
    """ Delete a user activity audit when user is logged out """
    try:
        UserAudit.objects.get(audit_key=request.session[defs.AUDITWARE_SESSION_KEY]).delete()
    except:
        pass

    log.info(_('User {0} logged out'.format(user.email)))


def latch_to_signals():
    """
    Latch to the signals we are interested in.
    """
    User = get_user_model()
    django_signals.user_logged_in.connect(user_audit_create, sender=User, dispatch_uid='user_audit_create_call_me_only_once_please')
    django_signals.user_logged_out.connect(user_audit_delete, sender=User, dispatch_uid='user_audit_delete_call_me_only_once_please')