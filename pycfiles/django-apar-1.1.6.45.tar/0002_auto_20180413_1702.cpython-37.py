# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/invitation/migrations/0002_auto_20180413_1702.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 401 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('invitation', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='invite',
       options={'verbose_name':'Invite', 
      'verbose_name_plural':'Invites'})]