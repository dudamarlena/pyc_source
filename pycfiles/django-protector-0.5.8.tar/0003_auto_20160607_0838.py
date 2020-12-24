# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s.lihobabin/projects/protector/django-protector/protector/migrations/0003_auto_20160607_0838.py
# Compiled at: 2017-07-18 04:51:58
from __future__ import unicode_literals
from django.db import migrations
import django.db.models.manager

class Migration(migrations.Migration):
    dependencies = [
     ('protector', '0002_auto_20160607_0827')]
    operations = [
     migrations.AlterModelManagers(name=b'restriction', managers=[
      (
       b'objects', django.db.models.manager.Manager())])]