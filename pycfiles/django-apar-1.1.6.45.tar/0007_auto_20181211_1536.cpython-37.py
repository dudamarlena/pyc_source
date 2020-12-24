# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/basemodels/migrations/0007_auto_20181211_1536.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 373 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('basemodels', '0006_auto_20181211_1351')]
    operations = [
     migrations.RenameModel(old_name='Tagulous_BaseModel_tags',
       new_name='Tag')]