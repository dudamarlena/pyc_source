# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/segments/migrations/0009_remove_basesegment_pages.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 359 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('segments', '0008_auto_20181213_1845')]
    operations = [
     migrations.RemoveField(model_name='basesegment',
       name='pages')]