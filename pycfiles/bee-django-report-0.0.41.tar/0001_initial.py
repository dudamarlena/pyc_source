# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0001_initial.py
# Compiled at: 2018-07-25 03:46:44
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'ClassWeek', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'class_id', models.IntegerField(null=True, verbose_name=b'班级id')),
      (
       b'year', models.IntegerField()),
      (
       b'week', models.IntegerField(null=True)),
      (
       b'type_int', models.IntegerField(default=0)),
      (
       b'start_date', models.DateField()),
      (
       b'end_date', models.DateField()),
      (
       b'live_mins', models.IntegerField()),
      (
       b'feed_count', models.IntegerField()),
      (
       b'live_days', models.IntegerField()),
      (
       b'live_count', models.IntegerField()),
      (
       b'last_user_section_id', models.IntegerField(null=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True, null=True)),
      (
       b'mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'classWeek_mentor', to=settings.AUTH_USER_MODEL)),
      (
       b'user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'classWeek_student', to=settings.AUTH_USER_MODEL, verbose_name=b'学生'))], options={b'ordering': [
                    b'created_at'], 
        b'db_table': b'bee_django_report_class_week'}),
     migrations.CreateModel(name=b'mentorScore', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'year', models.IntegerField()),
      (
       b'week', models.IntegerField(null=True)),
      (
       b'score', models.FloatField(null=True)),
      (
       b'rank', models.IntegerField(null=True)),
      (
       b'level', models.IntegerField(null=True)),
      (
       b'info', models.TextField(null=True)),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'created_at'], 
        b'db_table': b'bee_django_report_montor_score'})]