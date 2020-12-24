# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0048_userlivecomment.py
# Compiled at: 2018-09-04 03:04:36
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course', '0047_auto_20180813_1214')]
    operations = [
     migrations.CreateModel(name=b'UserLiveComment', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'comment', models.TextField(verbose_name=b'评论')),
      (
       b'submit_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name=b'提交日期')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'作者')),
      (
       b'user_live', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_course.UserLive'))])]