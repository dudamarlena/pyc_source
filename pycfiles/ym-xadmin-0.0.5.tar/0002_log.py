# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\migrations\0002_log.py
# Compiled at: 2018-12-16 22:27:14
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
     migrations.CreateModel(name=b'Log', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'action_time', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name=b'action time')),
      (
       b'ip_addr', models.GenericIPAddressField(blank=True, null=True, verbose_name=b'action ip')),
      (
       b'object_id', models.TextField(blank=True, null=True, verbose_name=b'object id')),
      (
       b'object_repr', models.CharField(max_length=200, verbose_name=b'object repr')),
      (
       b'action_flag', models.PositiveSmallIntegerField(verbose_name=b'action flag')),
      (
       b'message', models.TextField(blank=True, verbose_name=b'change message')),
      (
       b'content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'contenttypes.ContentType', verbose_name=b'content type')),
      (
       b'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'user'))], options={b'ordering': ('-action_time', ), 
        b'verbose_name': b'log entry', 
        b'verbose_name_plural': b'log entries'})]