# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0002_auto_20180112_1812.py
# Compiled at: 2018-01-12 05:12:50
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'Notice', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.TextField(verbose_name=b'须知标题')),
      (
       b'context', models.TextField(blank=True, null=True, verbose_name=b'须知内容')),
      (
       b'is_require', models.BooleanField(verbose_name=b'是否必选'))], options={b'ordering': [
                    b'-id'], 
        b'db_table': b'bee_django_exam_notice'}),
     migrations.AlterField(model_name=b'userexam', name=b'grade', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=b'bee_django_exam_grade', to=b'bee_django_exam.Grade', verbose_name=b'考试级别')),
     migrations.AddField(model_name=b'grade', name=b'notice', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'bee_django_exam.Notice', verbose_name=b'考试须知'))]