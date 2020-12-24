# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0002_user_follows_count.py
# Compiled at: 2015-12-21 18:12:44
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'follows_count', field=models.PositiveIntegerField(null=True), preserve_default=True)]