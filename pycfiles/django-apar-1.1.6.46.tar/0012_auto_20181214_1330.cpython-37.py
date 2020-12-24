# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0012_auto_20181214_1330.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 642 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0011_remove_basesegment_sort')]
    operations = [
     migrations.AlterModelOptions(name='pagesort',
       options={'ordering':[
       'sort'], 
      'verbose_name':'Page Sort',  'verbose_name_plural':'Pages Sort'}),
     migrations.AlterModelOptions(name='segmentsort',
       options={'ordering':[
       'sort'], 
      'verbose_name':'Segment Sort',  'verbose_name_plural':'Segments Sort'})]