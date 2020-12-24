# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0018_feed_type_id.py
# Compiled at: 2019-03-24 09:55:54
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0017_feedcomment_to_user')]
    operations = [
     migrations.AddField(model_name=b'feed', name=b'type_id', field=models.IntegerField(blank=True, null=True))]