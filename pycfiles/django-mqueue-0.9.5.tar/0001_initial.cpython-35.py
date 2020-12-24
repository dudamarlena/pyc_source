# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo78/mogo/mqueue/migrations/0001_initial.py
# Compiled at: 2017-09-27 04:05:25
# Size of source mod 2**32: 2405 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='MEvent', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'obj_pk', models.IntegerField(blank=True, null=True, verbose_name='Object primary key')),
      (
       'name', models.CharField(max_length=120, verbose_name='Name')),
      (
       'url', models.CharField(blank=True, max_length=255, verbose_name='Url')),
      (
       'admin_url', models.CharField(blank=True, max_length=255, verbose_name='Admin url')),
      (
       'notes', models.TextField(blank=True)),
      (
       'date_posted', models.DateTimeField(auto_now_add=True, verbose_name='Date posted')),
      (
       'event_class', models.CharField(blank=True, max_length=120, verbose_name='Class')),
      (
       'request', models.TextField(blank=True, verbose_name='Request')),
      (
       'bucket', models.CharField(blank=True, max_length=60, verbose_name='Bucket')),
      (
       'data', models.CharField(blank=True, max_length=120, verbose_name='Data')),
      (
       'scope', models.CharField(choices=[('superuser', 'Superuser'), ('staff', 'Staff'), ('users', 'Users'), ('public', 'Public')], default='superuser', max_length=18, verbose_name='Scope')),
      (
       'content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Content type')),
      (
       'user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='User'))], options={'ordering': ['-date_posted'], 
      'verbose_name_plural': 'Events', 
      'permissions': (('view_mevent', 'Can see Events'), ), 
      'verbose_name': 'Event'})]