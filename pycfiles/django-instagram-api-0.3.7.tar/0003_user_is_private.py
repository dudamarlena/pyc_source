# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0003_user_is_private.py
# Compiled at: 2015-12-22 02:18:41
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0002_user_follows_count')]
    operations = [
     migrations.AddField(model_name=b'user', name=b'is_private', field=models.NullBooleanField(verbose_name=b'Account is private'), preserve_default=True)]