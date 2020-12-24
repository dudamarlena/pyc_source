# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0005_userimage.py
# Compiled at: 2019-04-18 00:52:25
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('bee_django_course_simple', '0004_auto_20190417_1737')]
    operations = [
     migrations.CreateModel(name=b'UserImage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'image', models.ImageField(upload_to=b'course/%Y/%m/%d', verbose_name=b'图片')),
      (
       b'upload_at', models.DateTimeField(auto_now_add=True, verbose_name=b'上传时间')),
      (
       b'user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'simple_user_image', to=settings.AUTH_USER_MODEL))], options={b'db_table': b'bee_django_course_simple_user_image'})]