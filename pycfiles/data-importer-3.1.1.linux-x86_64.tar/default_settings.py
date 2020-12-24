# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/core/default_settings.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
try:
    from django.conf import settings
except ImportError:
    settings = {}

DATA_IMPORTER_TASK = False
DATA_IMPORTER_QUEUE = b'DataImporter'
DATA_IMPORTER_TASK_LOCK_EXPIRE = 1200
DATA_IMPORTER_EXCEL_DECODER = hasattr(settings, b'DATA_IMPORTER_EXCEL_DECODER') and settings.DATA_IMPORTER_EXCEL_DECODER or b'cp1252'
DATA_IMPORTER_DECODER = hasattr(settings, b'DATA_IMPORTER_DECODER') and settings.DATA_IMPORTER_DECODER or b'utf-8'