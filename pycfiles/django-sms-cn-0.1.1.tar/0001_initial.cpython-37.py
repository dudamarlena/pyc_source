# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/sms/migrations/0001_initial.py
# Compiled at: 2019-09-24 05:06:42
# Size of source mod 2**32: 1727 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Template',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'label', models.CharField(max_length=200, verbose_name='label')),
      (
       'code', models.CharField(max_length=50, unique=True, verbose_name='code')),
      (
       'content', models.TextField(blank=True, verbose_name='content'))],
       options={'verbose_name':'sms template', 
      'verbose_name_plural':'sms template'}),
     migrations.CreateModel(name='Log',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'mobile', models.CharField(max_length=15, verbose_name='mobile')),
      (
       'content', models.TextField(verbose_name='content')),
      (
       'is_success', models.BooleanField(default=True, verbose_name='is success')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'template', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='记录', to='sms.Template'))],
       options={'verbose_name':'sms log', 
      'verbose_name_plural':'sms log', 
      'ordering':[
       '-created']})]