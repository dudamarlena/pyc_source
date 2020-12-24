# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0018_auto_20180109_0942.py
# Compiled at: 2018-01-09 04:42:59
from __future__ import unicode_literals
from django.db import migrations, models
import pyas2.models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0017_auto_20170404_0730')]
    operations = [
     migrations.AlterField(model_name=b'partner', name=b'https_ca_cert', field=models.FileField(blank=True, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name=b'HTTPS Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'ca_cert', field=models.FileField(blank=True, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'certificate', field=models.FileField(upload_to=pyas2.models.get_certificate_path)),
     migrations.AlterField(model_name=b'publiccertificate', name=b'ca_cert', field=models.FileField(blank=True, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'publiccertificate', name=b'certificate', field=models.FileField(upload_to=pyas2.models.get_certificate_path))]