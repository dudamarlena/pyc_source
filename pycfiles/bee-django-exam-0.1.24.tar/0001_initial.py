# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0001_initial.py
# Compiled at: 2018-01-12 04:45:44
from __future__ import unicode_literals
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Grade', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'name', models.CharField(max_length=180, verbose_name=b'考级名称')),
      (
       b'order_by', models.IntegerField(blank=True, default=0, verbose_name=b'顺序')),
      (
       b'is_show', models.BooleanField(default=True, verbose_name=b'是否显示')),
      (
       b'cert_image', models.ImageField(null=True, storage=django.core.files.storage.FileSystemStorage(location=b'media/exam_cert'), upload_to=b''))], options={b'ordering': [
                    b'order_by'], 
        b'db_table': b'bee_django_exam_grade'}),
     migrations.CreateModel(name=b'UserExam', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'grade_title', models.CharField(max_length=180, null=True)),
      (
       b'created_at', models.DateTimeField(null=True)),
      (
       b'is_passed', models.BooleanField(default=False)),
      (
       b'result', models.CharField(blank=True, max_length=180, null=True, verbose_name=b'成绩')),
      (
       b'info', models.TextField(blank=True, null=True, verbose_name=b'其他')),
      (
       b'grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_django_exam_grade', to=b'bee_django_exam.Grade')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'bee_django_exam_user', to=settings.AUTH_USER_MODEL))], options={b'ordering': [
                    b'-created_at'], 
        b'db_table': b'bee_django_exam_user_exam'})]