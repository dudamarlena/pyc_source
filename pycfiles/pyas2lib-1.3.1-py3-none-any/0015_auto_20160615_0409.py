# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0015_auto_20160615_0409.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
import django.core.files.storage
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0014_auto_20160420_0515')]
    operations = [
     migrations.AlterField(model_name=b'partner', name=b'https_ca_cert', field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates', verbose_name=b'HTTPS Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'ca_cert', field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates', verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'certificate', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates')),
     migrations.AlterField(model_name=b'publiccertificate', name=b'ca_cert', field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates', verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'publiccertificate', name=b'certificate', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev'), upload_to=b'certificates'))]