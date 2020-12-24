# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sites/management.py
# Compiled at: 2019-02-14 00:35:17
"""
Creates the default Site object.
"""
from django.apps import apps as global_apps
from django.conf import settings
from django.core.management.color import no_style
from django.db import DEFAULT_DB_ALIAS, connections, router

def create_default_site(app_config, verbosity=2, interactive=True, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    try:
        Site = apps.get_model('sites', 'Site')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Site):
        return
    if not Site.objects.using(using).exists():
        if verbosity >= 2:
            print 'Creating example.com Site object'
        Site(pk=getattr(settings, 'SITE_ID', 1), domain='example.com', name='example.com').save(using=using)
        sequence_sql = connections[using].ops.sequence_reset_sql(no_style(), [Site])
        if sequence_sql:
            if verbosity >= 2:
                print 'Resetting sequence'
            with connections[using].cursor() as (cursor):
                for command in sequence_sql:
                    cursor.execute(command)