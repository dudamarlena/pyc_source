# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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