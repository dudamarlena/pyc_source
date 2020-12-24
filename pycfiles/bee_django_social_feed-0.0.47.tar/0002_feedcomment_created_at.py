# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0002_feedcomment_created_at.py
# Compiled at: 2018-05-29 05:43:54
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'feedcomment', name=b'created_at', field=models.DateTimeField(default=django.utils.timezone.now))]