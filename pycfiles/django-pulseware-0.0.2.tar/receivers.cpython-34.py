# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.mpro-virenv/sf3/lib/python3.4/site-packages/pulseware/receivers.py
# Compiled at: 2016-01-18 12:22:54
# Size of source mod 2**32: 369 bytes
from django.conf import settings
from django.db.models import signals
from django.apps import apps
from django.db import DEFAULT_DB_ALIAS
from .models import Heartbeat

def post_migrate_receiver(app_config, verbosity=2, interactive=False, using=DEFAULT_DB_ALIAS, **kwargs):
    """
    Finalize the website loading.
    """
    Heartbeat.objects.get_or_create(id=1)