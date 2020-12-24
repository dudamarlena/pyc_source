# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0010_auto_20180708_0959.py
# Compiled at: 2018-07-07 21:59:21
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0009_album_feed')]
    operations = [
     migrations.RemoveField(model_name=b'album', name=b'feed'),
     migrations.AddField(model_name=b'feed', name=b'album', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_social_feed.Album'))]