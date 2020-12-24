# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/listeners.py
# Compiled at: 2020-04-17 10:46:24
from django.db.models.signals import post_delete
from data_importer.models import FileHistory
import os
from django.conf import settings

def delete_filefield(sender, instance, **kwargs):
    """
    Automatically deleted files when records removed.
    """
    has_delete_config = hasattr(settings, 'DATA_IMPORTER_HISTORY')
    if has_delete_config and settings.DATA_IMPORTER_HISTORY == False:
        if os.path.exists(instance.filename.path):
            os.unlink(instance.filename.path)


post_delete.connect(delete_filefield, sender=FileHistory)