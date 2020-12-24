# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/sites/management.py
# Compiled at: 2018-07-11 18:15:30
"""
Creates the default Site object.
"""
from django.db.models import signals
from django.db import connections
from django.db import router
from django.contrib.sites.models import Site
from django.contrib.sites import models as site_app
from django.core.management.color import no_style

def create_default_site(app, created_models, verbosity, db, **kwargs):
    if Site in created_models and router.allow_syncdb(db, Site):
        if verbosity >= 2:
            print 'Creating example.com Site object'
        Site(pk=1, domain='example.com', name='example.com').save(using=db)
        sequence_sql = connections[db].ops.sequence_reset_sql(no_style(), [Site])
        if sequence_sql:
            if verbosity >= 2:
                print 'Resetting sequence'
            cursor = connections[db].cursor()
            for command in sequence_sql:
                cursor.execute(command)

    Site.objects.clear_cache()


signals.post_syncdb.connect(create_default_site, sender=site_app)