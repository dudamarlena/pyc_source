# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./pyas2/migrations/0014_auto_20160420_0515.py
# Compiled at: 2017-03-06 23:12:21
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('pyas2', '0013_auto_20160307_0233')]
    operations = [
     migrations.AddField(model_name=b'organization', name=b'confirmation_message', field=models.CharField(blank=True, help_text=b'Use this field to send a customized message in the MDN Confirmations for this Organization', max_length=300, null=True, verbose_name=b'Confirmation Message')),
     migrations.AddField(model_name=b'partner', name=b'confirmation_message', field=models.CharField(blank=True, help_text=b'Use this field to send a customized message in the MDN Confirmations for this Partner', max_length=300, null=True, verbose_name=b'Confirmation Message'))]