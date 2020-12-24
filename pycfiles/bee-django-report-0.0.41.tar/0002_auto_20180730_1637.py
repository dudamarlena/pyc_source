# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_report/migrations/0002_auto_20180730_1637.py
# Compiled at: 2018-07-30 04:37:58
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_report', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'MentorScoreWeek', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'year', models.IntegerField(verbose_name=b'年')),
      (
       b'week', models.IntegerField(null=True, verbose_name=b'第几周')),
      (
       b'score', models.FloatField(null=True, verbose_name=b'分数')),
      (
       b'rank', models.IntegerField(null=True)),
      (
       b'level', models.IntegerField(null=True)),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'备注')),
      (
       b'created_at', models.DateTimeField(auto_now_add=True)),
      (
       b'mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'created_at'], 
        b'db_table': b'bee_django_report_montor_score_week'}),
     migrations.RemoveField(model_name=b'mentorscore', name=b'mentor'),
     migrations.DeleteModel(name=b'mentorScore')]