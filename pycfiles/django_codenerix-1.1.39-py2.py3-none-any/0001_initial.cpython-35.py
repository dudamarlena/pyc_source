# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix/migrations/0001_initial.py
# Compiled at: 2017-12-18 07:03:26
# Size of source mod 2**32: 1515 bytes
from __future__ import unicode_literals
from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     ('contenttypes', '0002_remove_content_type_name'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Log', fields=[
      (
       'id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
      (
       'action_time', models.DateTimeField(auto_now=True, verbose_name='Date')),
      (
       'object_id', models.TextField(null=True, verbose_name='Object id', blank=True)),
      (
       'object_repr', models.CharField(max_length=200, verbose_name='Object repr')),
      (
       'action_flag', models.PositiveSmallIntegerField(verbose_name='Acción')),
      (
       'change_json', models.TextField(verbose_name='Json', blank=True)),
      (
       'change_txt', models.TextField(verbose_name='Txt', blank=True)),
      (
       'content_type', models.ForeignKey(on_delete=models.DO_NOTHING, blank=True, to='contenttypes.ContentType', null=True)),
      (
       'user', models.ForeignKey(on_delete=models.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL, null=True))], options={'permissions': (('list_log', 'Can list log'), ('detail_log', 'Can view log'))})]