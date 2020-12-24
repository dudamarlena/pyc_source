# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/cms-sample/dev_packages/djangocms-career/djangocms_career/migrations/0006_remove_post_is_public.py
# Compiled at: 2016-04-18 07:22:25
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('djangocms_career', '0005_auto_20160418_1202')]
    operations = [
     migrations.RemoveField(model_name=b'post', name=b'is_public')]