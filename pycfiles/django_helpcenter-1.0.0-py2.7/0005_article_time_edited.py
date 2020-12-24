# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/migrations/0005_article_time_edited.py
# Compiled at: 2016-09-30 00:56:02
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('helpcenter', '0004_auto_20160607_1234')]
    operations = [
     migrations.AddField(model_name=b'article', name=b'time_edited', field=models.DateTimeField(auto_now=True, null=True, verbose_name=b'time last modifed'))]