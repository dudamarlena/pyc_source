# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcos/rapid-django/src/rapid/migrations/0002_auto_20150918_1921.py
# Compiled at: 2015-09-18 15:21:14
from __future__ import unicode_literals
from django.db import models, migrations
from django_migration_fixture import fixture
import rapid

class Migration(migrations.Migration):
    dependencies = [
     ('rapid', '0001_initial')]
    operations = [
     migrations.RunPython(**fixture(rapid, [b'initial_data.json']))]