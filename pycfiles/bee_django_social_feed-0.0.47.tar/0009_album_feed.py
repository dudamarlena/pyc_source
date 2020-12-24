# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0009_album_feed.py
# Compiled at: 2018-07-04 08:34:25
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0008_album_status')]
    operations = [
     migrations.AddField(model_name=b'album', name=b'feed', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=b'bee_django_social_feed.Feed'))]