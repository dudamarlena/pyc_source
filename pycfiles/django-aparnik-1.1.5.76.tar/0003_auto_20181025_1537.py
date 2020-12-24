# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0003_auto_20181025_1537.py
# Compiled at: 2018-10-25 08:07:56
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0002_auto_20181025_1112')]
    operations = [
     migrations.AlterField(model_name=b'basesegment', name=b'pages', field=models.ManyToManyField(null=True, related_name=b'segment_pages', to=b'pages.Page', verbose_name=b'Page'))]