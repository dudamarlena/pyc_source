# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0005_auto_20160418_1202.py
# Compiled at: 2016-04-18 10:08:49
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_career', '0004_auto_20160418_1145')]
    operations = [
     migrations.AlterField(model_name=b'post', name=b'active_post', field=models.BooleanField(help_text=b"Check this if this is your active post. You won't have to add the end date in that case.", verbose_name=b'Active position?')),
     migrations.AlterField(model_name=b'post', name=b'description', field=models.TextField(help_text=b'Give a short description about your work and responsibilities.', max_length=2048, null=True, verbose_name=b'Description', blank=True)),
     migrations.AlterField(model_name=b'post', name=b'is_public', field=models.BooleanField(default=True, help_text=b"This flag will make the position public. Don't tick this if you want to make a draft.", verbose_name=b'Is public?'))]