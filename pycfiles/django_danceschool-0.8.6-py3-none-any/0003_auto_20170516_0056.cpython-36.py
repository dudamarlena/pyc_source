# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0003_auto_20170516_0056.py
# Compiled at: 2019-04-03 22:56:25
# Size of source mod 2**32: 1165 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0002_auto_20170512_1459')]
    operations = [
     migrations.AddField(model_name='event',
       name='uuid',
       field=models.UUIDField(default=(uuid.uuid4), editable=False, verbose_name='Unique Link ID')),
     migrations.AlterField(model_name='event',
       name='status',
       field=models.CharField(choices=[('D', 'Registration disabled'), ('O', 'Registration enabled'), ('K', 'Registration held closed (override default behavior)'), ('H', 'Registration held open (override default)'), ('L', 'Registration open, but hidden from registration page and calendar (link required to register)'), ('C', 'Hidden from registration page and registration closed, but visible on calendar.'), ('X', 'Event hidden and registration closed')], help_text='Set the registration status and visibility status of this event.', max_length=1))]