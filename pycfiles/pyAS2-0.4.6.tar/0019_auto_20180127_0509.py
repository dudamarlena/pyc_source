# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0019_auto_20180127_0509.py
# Compiled at: 2018-01-27 00:09:06
from __future__ import unicode_literals
from django.db import migrations, models
import pyas2.models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0018_auto_20180109_0942')]
    operations = [
     migrations.AlterField(model_name=b'mdn', name=b'file', field=models.CharField(max_length=500)),
     migrations.AlterField(model_name=b'partner', name=b'https_ca_cert', field=models.FileField(blank=True, max_length=500, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name=b'HTTPS Local CA Store')),
     migrations.AlterField(model_name=b'payload', name=b'file', field=models.CharField(max_length=500)),
     migrations.AlterField(model_name=b'privatecertificate', name=b'ca_cert', field=models.FileField(blank=True, max_length=500, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'certificate', field=models.FileField(max_length=500, upload_to=pyas2.models.get_certificate_path)),
     migrations.AlterField(model_name=b'publiccertificate', name=b'ca_cert', field=models.FileField(blank=True, max_length=500, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'publiccertificate', name=b'certificate', field=models.FileField(max_length=500, upload_to=pyas2.models.get_certificate_path))]