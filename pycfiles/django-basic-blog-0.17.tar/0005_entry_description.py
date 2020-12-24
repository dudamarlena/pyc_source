# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Projects/django-basic-blog/blog/migrations/0005_entry_description.py
# Compiled at: 2015-07-14 12:37:49
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('blog', '0004_entry_publicity')]
    operations = [
     migrations.AddField(model_name=b'entry', name=b'description', field=models.CharField(default=b'', max_length=200))]