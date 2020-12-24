# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/management/sites.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import print_function, unicode_literals
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import six
from djblets.siteconfig.models import SiteConfiguration
from reviewboard import get_version_string
from reviewboard.admin.siteconfig import settings_map, defaults

def init_siteconfig(app, created_models, verbosity, db=None, **kwargs):
    """Initialize the site configuration.

    This will create a SiteConfiguration object if one does not exist, or
    update the existing one with the current version number.
    """
    try:
        site = Site.objects.get_current()
    except Site.DoesNotExist:
        from django.contrib.sites.management import create_default_site
        create_default_site(app, created_models, verbosity, db=db)
        site = Site.objects.get_current()

    siteconfig, is_new = SiteConfiguration.objects.get_or_create(site=site)
    new_version = get_version_string()
    if is_new:
        if Site not in created_models:
            print(b'*** Migrating settings from settings_local.py to the database.')
        migrate_settings(siteconfig)
        if Site not in created_models:
            print(b'*** If you have previously configured Review Board through a ')
            print(b'*** settings_local.py file, please ensure that the migration ')
            print(b'*** was successful by verifying your settings at')
            print(b'*** %s://%s%sadmin/settings/' % (
             siteconfig.get(b'site_domain_method'),
             site.domain,
             settings.SITE_ROOT))
        siteconfig.version = new_version
        siteconfig.save()
    elif siteconfig.version != new_version:
        print(b'Upgrading Review Board from %s to %s' % (siteconfig.version,
         new_version))
        siteconfig.version = new_version
        siteconfig.save()


migration_table = {b'auth_require_sitewide_login': b'REQUIRE_SITEWIDE_LOGIN', 
   b'diffviewer_context_num_lines': b'DIFF_CONTEXT_NUM_LINES', 
   b'diffviewer_include_space_patterns': b'DIFF_INCLUDE_SPACE_PATTERNS', 
   b'diffviewer_paginate_by': b'DIFFVIEWER_PAGINATE_BY', 
   b'diffviewer_paginate_orphans': b'DIFFVIEWER_PAGINATE_ORPHANS', 
   b'diffviewer_syntax_highlighting': b'DIFF_SYNTAX_HIGHLIGHTING', 
   b'mail_send_review_mail': b'SEND_REVIEW_MAIL', 
   b'search_enable': b'ENABLE_SEARCH', 
   b'search_index_file': b'SEARCH_INDEX'}
migration_table.update(settings_map)
auth_backend_map = {b'django.contrib.auth.backends.ModelBackend': b'builtin', 
   b'reviewboard.accounts.backends.NISBackend': b'nis', 
   b'reviewboard.accounts.backends.LDAPBackend': b'ldap', 
   b'reviewboard.accounts.backends.HTTPDigestBackend': b'digest'}

def migrate_settings(siteconfig):
    """Migrate any settings we want in the database from the settings file."""
    for siteconfig_key, setting_data in six.iteritems(migration_table):
        if isinstance(setting_data, dict):
            setting_key = setting_data[b'key']
            serialize_func = setting_data.get(b'serialize_func', None)
        else:
            setting_key = setting_data
            serialize_func = None
        default = defaults.get(siteconfig_key, None)
        value = getattr(settings, setting_key, default)
        if serialize_func and six.callable(serialize_func):
            value = serialize_func(value)
        siteconfig.set(siteconfig_key, value)

    if type(settings.ADMINS[0]) == tuple:
        admin = settings.ADMINS[0]
    else:
        admin = settings.ADMINS
    siteconfig.set(b'site_admin_name', admin[0])
    siteconfig.set(b'site_admin_email', admin[1])
    remaining_backends = []
    known_backends = []
    for auth_backend in settings.AUTHENTICATION_BACKENDS:
        if auth_backend in auth_backend_map:
            known_backends.append(auth_backend)
        else:
            remaining_backends.append(auth_backend)

    if remaining_backends or len(known_backends) > 1:
        siteconfig.set(b'auth_backend', b'custom')
        siteconfig.set(b'auth_custom_backends', settings.AUTHENTICATION_BACKENDS)
    elif len(known_backends) == 1:
        siteconfig.set(b'auth_backend', auth_backend_map[known_backends[0]])
    else:
        siteconfig.set(b'auth_backend', b'builtin')
    return