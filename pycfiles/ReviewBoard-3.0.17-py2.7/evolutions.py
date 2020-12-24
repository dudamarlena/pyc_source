# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/management/evolutions.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.management import call_command
from django_evolution import models as django_evolution
from reviewboard.diffviewer.models import FileDiff

def init_evolutions(app, created_models, **kwargs):
    """Attempt to initialize the Django Evolution schema signatures.

    This attempts to initialize the evolution signatures to sane values. This
    works around the issue where a first syncdb with Django Evolution (even on
    existing databases) will cause Django Evolution to assume the database is
    the most up to date, even if it's not. This will break the database. Our
    workarounds prevent this by starting off with sane values and doing some
    smart checks.
    """
    if FileDiff in created_models:
        return
    else:
        try:
            latest_version = django_evolution.Version.objects.latest(b'when')
        except django_evolution.Version.DoesNotExist:
            latest_version = None

        if latest_version:
            try:
                FileDiff.objects.filter(parent_diff64=b'')
                return
            except:
                django_evolution.Version.objects.all().delete()
                django_evolution.Evolution.objects.all().delete()

        call_command(b'loaddata', b'admin/fixtures/initial_evolution_schema.json', verbosity=0)
        return