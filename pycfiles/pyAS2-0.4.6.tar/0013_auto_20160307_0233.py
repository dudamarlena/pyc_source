# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0013_auto_20160307_0233.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
import django.core.files.storage
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0012_auto_20151006_0526')]
    operations = [
     migrations.AlterField(model_name=b'organization', name=b'as2_name', field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name=b'AS2 Identifier')),
     migrations.AlterField(model_name=b'organization', name=b'email_address', field=models.EmailField(blank=True, max_length=254, null=True)),
     migrations.AlterField(model_name=b'organization', name=b'name', field=models.CharField(max_length=100, verbose_name=b'Organization Name')),
     migrations.AlterField(model_name=b'partner', name=b'email_address', field=models.EmailField(blank=True, max_length=254, null=True)),
     migrations.AlterField(model_name=b'partner', name=b'https_ca_cert', field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates', verbose_name=b'HTTPS Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'ca_cert', field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates', verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'privatecertificate', name=b'certificate', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates')),
     migrations.AlterField(model_name=b'publiccertificate', name=b'ca_cert', field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates', verbose_name=b'Local CA Store')),
     migrations.AlterField(model_name=b'publiccertificate', name=b'certificate', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/dj93'), upload_to=b'certificates'))]