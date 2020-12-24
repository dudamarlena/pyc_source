# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0008_auto_20181211_1552.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations
import tagulous.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0007_auto_20181211_1536')]
    operations = [
     migrations.AlterField(model_name=b'basemodel', name=b'tags', field=tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, help_text=b'Enter a comma-separated tag string', to=b'basemodels.Tag'))]