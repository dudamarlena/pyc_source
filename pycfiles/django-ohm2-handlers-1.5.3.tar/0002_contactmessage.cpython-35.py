# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/migrations/0002_contactmessage.py
# Compiled at: 2017-01-24 23:12:21
# Size of source mod 2**32: 1234 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('ohm2_handlers', '0001_initial')]
    operations = [
     migrations.CreateModel(name='ContactMessage', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=2048, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'subject', models.IntegerField(choices=[(1, 'Other'), (2, 'Support'), (3, 'Bug report'), (4, 'Feature request'), (5, 'Information'), (6, 'Inquiries')], default=1)),
      (
       'email', models.EmailField(max_length=254)),
      (
       'message', models.TextField()),
      (
       'ip_address', models.GenericIPAddressField())], options={'abstract': False})]