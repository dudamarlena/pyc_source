# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0012_auto_20160215_0123.py
# Compiled at: 2016-02-14 17:23:13
from __future__ import unicode_literals
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0011_auto_20160213_0338')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'followers_count', field=models.PositiveIntegerField(null=True, db_index=True), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'follows_count', field=models.PositiveIntegerField(null=True, db_index=True), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'is_private', field=models.NullBooleanField(db_index=True, verbose_name=b'Account is private'), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'media_count', field=models.PositiveIntegerField(null=True, db_index=True), preserve_default=True)]