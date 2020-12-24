# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-users/vkontakte_users/migrations/0002_auto_20160213_0238.py
# Compiled at: 2016-02-12 18:38:10
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('vkontakte_users', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'instagram', field=models.CharField(default=b'', max_length=30), preserve_default=False),
     migrations.AddField(model_name=b'user', name=b'is_banned', field=models.BooleanField(default=False, verbose_name=b'Забанен'), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'is_deleted', field=models.BooleanField(default=False, verbose_name=b'Удален'), preserve_default=True),
     migrations.AddField(model_name=b'user', name=b'nickname', field=models.CharField(default=b'', max_length=32), preserve_default=False),
     migrations.AddField(model_name=b'user', name=b'schools', field=models.TextField(default=b''), preserve_default=False),
     migrations.AddField(model_name=b'user', name=b'universities', field=models.TextField(default=b''), preserve_default=False),
     migrations.AlterField(model_name=b'user', name=b'bdate', field=models.CharField(max_length=10), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'facebook', field=models.CharField(max_length=18), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'facebook_name', field=models.CharField(max_length=50), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'faculty_name', field=models.CharField(max_length=255), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'first_name', field=models.CharField(max_length=32), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'has_avatar', field=models.BooleanField(default=True, db_index=True, verbose_name=b'Есть аватар'), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'home_phone', field=models.CharField(max_length=24), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'is_deactivated', field=models.BooleanField(default=False, db_index=True, verbose_name=b'Деактивирован'), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'last_name', field=models.CharField(max_length=32), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'livejournal', field=models.CharField(max_length=31), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'mobile_phone', field=models.CharField(max_length=24), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'screen_name', field=models.CharField(max_length=32, db_index=True), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'skype', field=models.CharField(max_length=32), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'twitter', field=models.CharField(max_length=15), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'university_name', field=models.CharField(max_length=255), preserve_default=True)]