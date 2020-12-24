# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/xadmin/migrations/0002_log.py
# Compiled at: 2018-01-28 08:42:20
# Size of source mod 2**32: 1849 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('xadmin', '0001_initial')]
    operations = [
     migrations.CreateModel(name='Log',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'action_time', models.DateTimeField(default=(django.utils.timezone.now), editable=False, verbose_name='action time')),
      (
       'ip_addr', models.GenericIPAddressField(blank=True, null=True, verbose_name='action ip')),
      (
       'object_id', models.TextField(blank=True, null=True, verbose_name='object id')),
      (
       'object_repr', models.CharField(max_length=200, verbose_name='object repr')),
      (
       'action_flag', models.PositiveSmallIntegerField(verbose_name='action flag')),
      (
       'message', models.TextField(blank=True, verbose_name='change message')),
      (
       'content_type', models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to='contenttypes.ContentType', verbose_name='content type')),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL), verbose_name='user'))],
       options={'ordering':('-action_time', ), 
      'verbose_name':'log entry', 
      'verbose_name_plural':'log entries'})]