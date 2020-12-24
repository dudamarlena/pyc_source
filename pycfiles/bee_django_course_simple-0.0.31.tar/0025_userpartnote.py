# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0025_userpartnote.py
# Compiled at: 2019-05-30 02:02:30
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course_simple', '0024_userpart_question_correct_count')]
    operations = [
     migrations.CreateModel(name=b'UserPartNote', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'note', models.TextField(verbose_name=b'学习笔记')),
      (
       b'is_open', models.BooleanField(default=True, verbose_name=b'公开笔记')),
      (
       b'created_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'updated_at', models.DateTimeField(default=django.utils.timezone.now)),
      (
       b'is_stick', models.BooleanField(default=False, verbose_name=b'是否置顶')),
      (
       b'is_digest', models.BooleanField(default=False, verbose_name=b'是否精华')),
      (
       b'part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_course_simple.Part')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_course_simple_userpartnote', 
        b'verbose_name': b'用户笔记'})]