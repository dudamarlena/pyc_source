# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Aaswaini Dev\PycharmProjects\FinanceCRM\apps\csv_importer\models.py
# Compiled at: 2020-04-22 11:08:45
# Size of source mod 2**32: 340 bytes
from django.db import models

class CSVUploadModel(models.Model):
    csv_upload_compulsory_fields = []
    fk_handle_by_id = []

    class Meta:
        abstract = True