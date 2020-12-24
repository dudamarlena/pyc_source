# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Aaswaini Dev\PycharmProjects\FinanceCRM\apps\csv_importer\admin.py
# Compiled at: 2020-04-22 10:59:46
# Size of source mod 2**32: 698 bytes
from django.contrib import admin
from apps.csv_importer.models import CSVUploadModel

class CsvUploadAdmin(admin.ModelAdmin):
    allow_csv_upload = True

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        if not isinstance(model(), CSVUploadModel):
            raise NotImplementedError('model must an instance of CSVUploadModel')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['allow_csv_upload'] = self.allow_csv_upload
        return super().changelist_view(request,
          extra_context=extra_context)