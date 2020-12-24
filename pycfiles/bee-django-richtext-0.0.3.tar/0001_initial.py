# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_richtext/migrations/0001_initial.py
# Compiled at: 2019-11-19 03:23:08
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'RichTextImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'app_name', models.CharField(max_length=180, null=True, verbose_name=b'app名')),
      (
       b'model_name', models.CharField(max_length=180, null=True, verbose_name=b'model名')),
      (
       b'image', models.ImageField(upload_to=b'bee_django_richtext/image', verbose_name=b'图片')),
      (
       b'upload_at', models.DateTimeField(auto_now_add=True, verbose_name=b'时间')),
      (
       b'user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={b'db_table': b'bee_django_richtext_image'})]