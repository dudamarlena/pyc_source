# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/migrations/0001_initial.py
# Compiled at: 2018-10-27 05:33:58
# Size of source mod 2**32: 1406 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='Book',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=10)),
      (
       'written', models.DateTimeField(default=(django.utils.timezone.now))),
      (
       'is_published', models.BooleanField(default=False)),
      (
       'rating', models.FloatField(null=True)),
      (
       'price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
      (
       'object_id', models.PositiveIntegerField(null=True)),
      (
       'author', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL))),
      (
       'content_type', models.ForeignKey(null=True, on_delete=(django.db.models.deletion.CASCADE), to='contenttypes.ContentType'))])]