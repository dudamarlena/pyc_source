# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0024_userparentrelation.py
# Compiled at: 2019-06-30 03:21:51
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_user', '0023_userprofile_wxapp_openid')]
    operations = [
     migrations.CreateModel(name=b'UserParentRelation', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'parent', to=settings.AUTH_USER_MODEL, verbose_name=b'家长')),
      (
       b'student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'student', to=settings.AUTH_USER_MODEL, verbose_name=b'学生'))], options={b'ordering': [
                    b'pk'], 
        b'db_table': b'bee_django_user_parent'})]