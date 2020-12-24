# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/forms.py
# Compiled at: 2020-04-17 10:46:24
import os
from django import forms
from data_importer.models import FileHistory
from data_importer.tasks import DataImpoterTask
try:
    import celery
    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False

class FileUploadForm(forms.ModelForm):
    is_task = True
    importer = None

    class Meta:
        model = FileHistory
        fields = ('file_upload', )