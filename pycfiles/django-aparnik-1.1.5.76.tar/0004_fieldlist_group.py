# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/managements/migrations/0004_fieldlist_group.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     ('managements', '0003_auto_20181126_1322')]
    operations = [
     migrations.AddField(model_name=b'fieldlist', name=b'group', field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=b'auth.Group', verbose_name=b'group'), preserve_default=False)]