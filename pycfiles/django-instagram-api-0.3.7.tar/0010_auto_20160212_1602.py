# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-instagram-api/instagram_api/migrations/0010_auto_20160212_1602.py
# Compiled at: 2016-02-12 08:16:42
from __future__ import unicode_literals
from django.db import models, migrations
import m2m_history.fields

class Migration(migrations.Migration):
    dependencies = [
     ('instagram_api', '0009_auto_20160212_1454')]
    operations = [
     migrations.AlterField(model_name=b'user', name=b'followers', field=m2m_history.fields.ManyToManyHistoryField(related_name=b'follows', to=b'instagram_api.User'), preserve_default=True)]