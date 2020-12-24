# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/guestlist/migrations/0002_guestlistname_notes.py
# Compiled at: 2019-04-03 22:56:31
# Size of source mod 2**32: 567 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('guestlist', '0001_initial')]
    operations = [
     migrations.AddField(model_name='guestlistname',
       name='notes',
       field=models.CharField(blank=True, help_text='These will be included on the list for reference.', max_length=200, null=True, verbose_name='Notes (optional)'))]