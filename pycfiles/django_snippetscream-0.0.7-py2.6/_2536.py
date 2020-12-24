# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snippetscream/_2536.py
# Compiled at: 2011-09-19 04:39:10
from django.conf import settings
from django.db.models import signals
from django.contrib.sites.models import Site
from django.contrib.sites import models as site_app
from django.contrib.sites.management import create_default_site as orig_default_site

def create_default_site(app, created_models, verbosity, db, **kwargs):
    name = kwargs.pop('name', None)
    domain = kwargs.pop('domain', None)
    if not name:
        name = getattr(settings, 'DEFAULT_SITE_NAME', 'example.com')
    if not domain:
        domain = getattr(settings, 'DEFAULT_SITE_DOMAIN', 'localhost:8000')
    if Site in created_models:
        if verbosity >= 2:
            print 'Creating default Site object:\nname: %s\ndomain: %s' % (name, domain)
        s = Site(domain=domain, name=name)
        s.save(using=db)
    Site.objects.clear_cache()
    return


if getattr(settings, 'CREATE_DEFAULT_SITE', False):
    signals.post_syncdb.disconnect(orig_default_site, sender=site_app)
    signals.post_syncdb.connect(create_default_site, sender=site_app, dispatch_uid='snippetscream._2536.create_default_site')