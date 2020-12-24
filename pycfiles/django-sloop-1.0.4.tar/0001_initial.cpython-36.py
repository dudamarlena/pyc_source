# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/migrations/0001_initial.py
# Compiled at: 2019-08-14 11:46:19
# Size of source mod 2**32: 1359 bytes
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone
from django_sloop.settings import DJANGO_SLOOP_SETTINGS

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(DJANGO_SLOOP_SETTINGS['DEVICE_MODEL'])]
    operations = [
     migrations.CreateModel(name='PushMessage',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'body', models.TextField()),
      (
       'data', models.TextField()),
      (
       'sns_message_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
      (
       'sns_response', models.TextField()),
      (
       'date_created', models.DateTimeField(default=(django.utils.timezone.now))),
      (
       'date_updated', models.DateTimeField(auto_now=True)),
      (
       'device', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='push_messages', to=(DJANGO_SLOOP_SETTINGS['DEVICE_MODEL'])))],
       options={'verbose_name':'Push Notification', 
      'verbose_name_plural':'Push Notifications'})]