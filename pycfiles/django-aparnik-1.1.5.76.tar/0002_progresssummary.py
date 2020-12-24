# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/progresses/migrations/0002_progresssummary.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('courses', '0005_remove_course_is_free'),
     ('progresses', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'ProgressSummary', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'percentage', models.IntegerField(verbose_name=b'Percentage')),
      (
       b'model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'progress_summaries', to=b'courses.Course', verbose_name=b'Models')),
      (
       b'user_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'progress_user', to=settings.AUTH_USER_MODEL, verbose_name=b'User'))], options={b'verbose_name': b'Progress Summary', 
        b'verbose_name_plural': b'Progress Summary'})]