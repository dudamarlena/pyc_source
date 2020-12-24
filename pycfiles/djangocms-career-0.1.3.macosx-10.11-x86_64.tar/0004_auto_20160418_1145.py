# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0004_auto_20160418_1145.py
# Compiled at: 2016-04-18 05:45:36
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_career', '0003_auto_20160418_1143')]
    operations = [
     migrations.RenameField(model_name=b'post', old_name=b'is_active', new_name=b'active_post'),
     migrations.AddField(model_name=b'post', name=b'is_public', field=models.BooleanField(default=True, help_text=b"This flag will make the position public. Don't tick this if you want to make a draft.", verbose_name=b'Is public?'), preserve_default=False)]