# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0004_auto_20170428_0850.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 1164 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0003_auto_20170418_1515')]
    operations = [
     migrations.AddField(model_name='sliderelementtexten', name='name_file', field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Name')),
     migrations.AddField(model_name='sliderelementtextes', name='name_file', field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Name')),
     migrations.AddField(model_name='staticheaderelementtexten', name='name_file', field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Name')),
     migrations.AddField(model_name='staticheaderelementtextes', name='name_file', field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Name'))]