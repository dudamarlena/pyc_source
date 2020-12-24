# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0008_album_status.py
# Compiled at: 2018-07-01 23:11:57
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0007_auto_20180702_0732')]
    operations = [
     migrations.AddField(model_name=b'album', name=b'status', field=models.IntegerField(default=0))]