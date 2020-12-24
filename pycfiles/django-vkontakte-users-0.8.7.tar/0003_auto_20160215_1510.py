# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-users/vkontakte_users/migrations/0003_auto_20160215_1510.py
# Compiled at: 2016-02-26 12:17:06
from __future__ import unicode_literals
from django.db import models, migrations
import annoying.fields

class Migration(migrations.Migration):
    dependencies = [
     ('vkontakte_users', '0002_auto_20160213_0238')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'schools', field=annoying.fields.JSONField(null=True, blank=True), preserve_default=True),
     migrations.AlterField(model_name=b'user', name=b'universities', field=annoying.fields.JSONField(null=True, blank=True), preserve_default=True)]