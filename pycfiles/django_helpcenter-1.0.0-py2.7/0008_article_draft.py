# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0008_article_draft.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0007_auto_20160715_1922')]
    operations = [
     migrations.AddField(model_name=b'article', name=b'draft', field=models.BooleanField(default=False, help_text=b'Marking an article as a draft will hide it from users.', verbose_name=b'article is a draft'))]