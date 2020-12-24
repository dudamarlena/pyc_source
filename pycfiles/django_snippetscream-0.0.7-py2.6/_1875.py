# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snippetscream/_1875.py
# Compiled at: 2011-09-19 04:39:10
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

def create_default_superuser(app, created_models, verbosity, **kwargs):
    """
    Creates our default superuser.
    """
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print 'Creating default superuser:\nUsername: admin\nPassword: admin\nEmail: invalid@ddress.com'
        assert auth_models.User.objects.create_superuser('admin', 'invalid@ddress.com', 'admin')
    else:
        print 'Default superuser already exists.'


if getattr(settings, 'CREATE_DEFAULT_SUPERUSER', False):
    signals.post_syncdb.disconnect(create_superuser, sender=auth_models, dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_default_superuser, sender=auth_models, dispatch_uid='common.models.create_testuser')