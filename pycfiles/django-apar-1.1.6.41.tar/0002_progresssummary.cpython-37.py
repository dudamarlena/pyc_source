# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/progresses/migrations/0002_progresssummary.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1237 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('courses', '0005_remove_course_is_free'),
     ('progresses', '0001_initial')]
    operations = [
     migrations.CreateModel(name='ProgressSummary',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'percentage', models.IntegerField(verbose_name='Percentage')),
      (
       'model', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='progress_summaries', to='courses.Course', verbose_name='Models')),
      (
       'user_obj', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='progress_user', to=(settings.AUTH_USER_MODEL), verbose_name='User'))],
       options={'verbose_name':'Progress Summary', 
      'verbose_name_plural':'Progress Summary'})]