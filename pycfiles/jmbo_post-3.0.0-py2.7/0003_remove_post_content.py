# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/post/migrations/0003_remove_post_content.py
# Compiled at: 2017-07-03 11:37:50
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('post', '0002_post_markup')]
    operations = [
     migrations.RemoveField(model_name=b'post', name=b'content')]