# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0012_auto_20151006_0526.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0011_auto_20150427_1029')]
    operations = [
     migrations.AddField(model_name=b'publiccertificate', name=b'verify_cert', field=models.BooleanField(default=True, help_text=b'Uncheck this option to disable certificate verification.', verbose_name=b'Verify Certificate'), preserve_default=True),
     migrations.AlterField(model_name=b'message', name=b'mdn_mode', field=models.CharField(max_length=5, null=True, choices=[('SYNC', 'Synchronous'), ('ASYNC', 'Asynchronous')]), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'as2_name', field=models.CharField(max_length=100, serialize=False, verbose_name=b'AS2 Identifier', primary_key=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'cmd_receive', field=models.TextField(help_text=b'Command executed after successful message receipt, replacements are $filename, $fullfilename, $sender, $recevier, $messageid and any message header such as $Subject', null=True, verbose_name=b'Command on Message Receipt', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'cmd_send', field=models.TextField(help_text=b'Command executed after successful message send, replacements are $filename, $sender, $recevier, $messageid and any message header such as $Subject', null=True, verbose_name=b'Command on Message Send', blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'partner', name=b'name', field=models.CharField(max_length=100, verbose_name=b'Partner Name'), preserve_default=True)]