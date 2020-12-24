# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/support.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import base64, sys, time
from datetime import datetime
from hashlib import sha1
from django.conf import settings
from django.contrib.auth.models import User
from djblets.siteconfig.models import SiteConfiguration
from reviewboard import get_package_version

def get_install_key():
    """Return the installation key for this server."""
    return sha1(settings.SECRET_KEY).hexdigest()


def _norm_siteconfig_value(siteconfig, key):
    """Normalize site configuration values to strip extra quotation marks."""
    value = siteconfig.get(key)
    if value in ('""', "''", None):
        value = b''
    return value


def serialize_support_data(request=None, force_is_admin=False):
    """Serialize support data into a base64-encoded string."""
    siteconfig = SiteConfiguration.objects.get_current()
    is_admin = force_is_admin or request is not None and request.user.is_staff
    return base64.b64encode((b'\t').join([
     get_install_key(),
     b'%d' % is_admin,
     siteconfig.site.domain,
     _norm_siteconfig_value(siteconfig, b'site_admin_name'),
     _norm_siteconfig_value(siteconfig, b'site_admin_email'),
     get_package_version(),
     b'%d' % User.objects.filter(is_active=True).count(),
     b'%d' % int(time.mktime(datetime.now().timetuple())),
     _norm_siteconfig_value(siteconfig, b'company'),
     b'%s.%s.%s' % sys.version_info[:3]]))


def get_default_support_url(request=None, force_is_admin=False):
    """Return the URL for the default Review Board support page."""
    siteconfig = SiteConfiguration.objects.get_current()
    if siteconfig.get(b'send_support_usage_stats'):
        support_data = serialize_support_data(request, force_is_admin)
    else:
        support_data = b''
    return settings.DEFAULT_SUPPORT_URL % {b'support_data': support_data}


def get_register_support_url(request=None, force_is_admin=False):
    """Return the URL for registering the Review Board support page."""
    siteconfig = SiteConfiguration.objects.get_current()
    if siteconfig.get(b'send_support_usage_stats'):
        support_data = serialize_support_data(request, force_is_admin)
    else:
        support_data = b''
    return settings.REGISTER_SUPPORT_URL % {b'support_data': support_data}


def get_support_url(request):
    """Return the URL for the configured support page."""
    siteconfig = SiteConfiguration.objects.get_current()
    return siteconfig.get(b'support_url') or get_default_support_url(request)