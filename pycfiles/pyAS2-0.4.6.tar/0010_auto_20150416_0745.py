# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pyas2/migrations/0010_auto_20150416_0745.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations
import django.core.files.storage

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0009_auto_20150317_1324')]
    operations = [
     migrations.AlterField(model_name=b'partner', name=b'cmd_receive', field=models.TextField(help_text=b'Command exectued after successful message receipt, replacements are $filename, $fullfilename, $sender, $recevier, $messageid and any messsage header such as $subject', null=True, verbose_name=b'Command on Message Receipt', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'cmd_send', field=models.TextField(help_text=b'Command exectued after successful message send, replacements are $filename, $sender, $recevier, $messageid and any messsage header such as $subject', null=True, verbose_name=b'Command on Message Send', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'https_ca_cert', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/AS2App/djproject'), upload_to=b'certificates', null=True, verbose_name=b'HTTPS Local CA Store', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'privatecertificate', name=b'ca_cert', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/AS2App/djproject'), upload_to=b'certificates', null=True, verbose_name=b'Local CA Store', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'privatecertificate', name=b'certificate', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/AS2App/djproject'), upload_to=b'certificates'), preserve_default=True),
     migrations.AlterField(model_name=b'publiccertificate', name=b'ca_cert', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/AS2App/djproject'), upload_to=b'certificates', null=True, verbose_name=b'Local CA Store', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'publiccertificate', name=b'certificate', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/Users/abhishekram/Documents/work/Research/AS2App/djproject'), upload_to=b'certificates'), preserve_default=True)]