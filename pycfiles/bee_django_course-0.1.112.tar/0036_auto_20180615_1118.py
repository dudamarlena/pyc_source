# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0036_auto_20180615_1118.py
# Compiled at: 2018-06-26 00:36:23
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course', '0035_auto_20180611_1624')]
    operations = [
     migrations.CreateModel(name=b'UserSectionNote', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'note', models.TextField(verbose_name=b'笔记')),
      (
       b'is_open', models.BooleanField(default=True, verbose_name=b'是否公开')),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'updated_at', models.DateTimeField(default=django.utils.timezone.now))]),
     migrations.AlterField(model_name=b'section', name=b'has_videowork', field=models.BooleanField(default=True, verbose_name=b'是否需要视频录制')),
     migrations.AddField(model_name=b'usersectionnote', name=b'section', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.Section')),
     migrations.AddField(model_name=b'usersectionnote', name=b'user', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]