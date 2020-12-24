# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_user/migrations/0017_userprofile_is_pause.py
# Compiled at: 2019-04-07 23:17:34
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_user', '0016_userprofile_avatar')]
    operations = [
     migrations.AddField(model_name=b'userprofile', name=b'is_pause', field=models.BooleanField(default=False, verbose_name=b'暂停'))]