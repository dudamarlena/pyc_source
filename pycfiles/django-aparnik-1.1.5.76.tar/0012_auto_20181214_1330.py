# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0012_auto_20181214_1330.py
# Compiled at: 2018-12-14 08:14:47
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0011_remove_basesegment_sort')]
    operations = [
     migrations.AlterModelOptions(name=b'pagesort', options={b'ordering': [b'sort'], b'verbose_name': b'Page Sort', b'verbose_name_plural': b'Pages Sort'}),
     migrations.AlterModelOptions(name=b'segmentsort', options={b'ordering': [b'sort'], b'verbose_name': b'Segment Sort', b'verbose_name_plural': b'Segments Sort'})]