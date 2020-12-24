# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/syre/work/django-thema/thema/migrations/0002_themacategory_notes.py
# Compiled at: 2018-03-01 08:33:10
# Size of source mod 2**32: 439 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('thema', '0001_initial')]
    operations = [
     migrations.AddField(model_name='themacategory',
       name='notes',
       field=models.TextField(default=''))]