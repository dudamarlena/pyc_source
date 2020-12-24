# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/monobot/sync/tickettest/simpletickets/migrations/0001_initial.py
# Compiled at: 2016-09-18 18:17:24
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone, simpletickets.models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name=b'Ticket', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'ticket_number', models.CharField(max_length=8, null=True, blank=True)),
      (
       b'ticket_type', models.IntegerField(default=2, choices=[(1, 'Inform about an error'), (2, 'Problem'), (3, 'Propose a sugestion'), (4, 'Others')])),
      (
       b'severity', models.IntegerField(default=3, choices=[(1, 'Critical'), (2, 'Very important'), (3, 'Important'), (4, 'Normal')])),
      (
       b'state', models.IntegerField(default=1, choices=[(1, 'new'), (2, 'assigned'), (3, 'solved'), (4, 'closed')])),
      (
       b'description', models.TextField(default=b'...', verbose_name=b'Description')),
      (
       b'attachment', models.FileField(null=True, upload_to=simpletickets.models.uploadAttachment, blank=True)),
      (
       b'resolution_text', models.TextField(default=b'', verbose_name=b'Resolution text')),
      (
       b'creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Creation Date')),
      (
       b'modification_date', models.DateTimeField(null=True, verbose_name=b'Last Modification Date', blank=True)),
      (
       b'resolution_date', models.DateTimeField(null=True, verbose_name=b'Resolution date', blank=True)),
      (
       b'resolution_delta', models.FloatField(null=True, verbose_name=b'delayed time in seconds', blank=True)),
      (
       b'staff', models.ForeignKey(related_name=b'usrStaff', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
      (
       b'user', models.ForeignKey(to=settings.AUTH_USER_MODEL))], options={b'ordering': ('state', 'severity', 'creation_date'), 
        b'verbose_name': b'Ticket', 
        b'verbose_name_plural': b'Tickets'})]