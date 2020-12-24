# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/migrations/0002_book_genre.py
# Compiled at: 2017-06-03 04:29:30
# Size of source mod 2**32: 502 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0001_initial')]
    operations = [
     migrations.AddField(model_name='book',
       name='genre',
       field=models.PositiveIntegerField(choices=[(1, 'Drama'), (2, 'Comics'), (3, 'Other')], null=True, blank=True))]