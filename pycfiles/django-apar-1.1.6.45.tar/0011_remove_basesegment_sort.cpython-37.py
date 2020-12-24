# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0011_remove_basesegment_sort.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 357 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0010_basesegment_pages')]
    operations = [
     migrations.RemoveField(model_name='basesegment',
       name='sort')]