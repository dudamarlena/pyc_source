# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0007_auto_20150313_0707.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations
import django.core.files.storage

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0006_auto_20150313_0548')]
    operations = [
     migrations.AddField(model_name=b'message', name=b'reties', field=models.IntegerField(null=True), preserve_default=True),
     migrations.AlterField(model_name=b'message', name=b'status', field=models.CharField(max_length=2, choices=[('S', 'Success'), ('E', 'Error'), ('W', 'Warning'), ('P', 'Pending'), ('R', 'Retry'), ('IP', 'In Process')]), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'cmd_receive', field=models.CharField(help_text=b'Command exectued after successful message receipt, replacements are ${filename}, ${fullfilename}, ${subject}, ${sender}, ${recevier}, ${messageid}', max_length=255, null=True, verbose_name=b'Command on Message Receipt', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'cmd_send', field=models.CharField(help_text=b'Command exectued after successful message send, replacements are ${filename}, ${subject}, ${sender}, ${recevier}, ${messageid}', max_length=255, null=True, verbose_name=b'Command on Message Send', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'encryption', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Encrypt Message', choices=[('des_ede3_cbc', '3DES'), ('des_ede_cbc', 'DES'), ('rc2_40_cbc', 'RC2-40'), ('rc4', 'RC4-40'), ('aes_128_cbc', 'AES-128'), ('aes_192_cbc', 'AES-192'), ('aes_256_cbc', 'AES-256')]), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'http_auth', field=models.BooleanField(default=False, verbose_name=b'Enable Authentication'), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'https_ca_cert', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), upload_to=b'certificates', null=True, verbose_name=b'HTTPS Local CA Store', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'keep_filename', field=models.BooleanField(default=False, help_text=b'Use Original Filename to to store file on receipt, use this option only if you are sure partner sends unique names', verbose_name=b'Keep Original Filename'), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'signature', field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'Sign Message', choices=[('sha1', 'SHA-1')]), preserve_default=True),
     migrations.AlterField(model_name=b'privatecertificate', name=b'ca_cert', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), upload_to=b'certificates', null=True, verbose_name=b'Local CA Store', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'publiccertificate', name=b'ca_cert', field=models.FileField(storage=django.core.files.storage.FileSystemStorage(base_url=b'/pyas2', location=b'/opt/pyapp/djproject'), upload_to=b'certificates', null=True, verbose_name=b'Local CA Store', blank=True), preserve_default=True)]