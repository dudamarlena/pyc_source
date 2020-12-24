# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0012_auto_20180709_1210.py
# Compiled at: 2018-07-09 00:10:56
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0011_auto_20180709_1103')]
    operations = [
     migrations.AddField(model_name=b'feedimage', name=b'medium_url', field=models.CharField(blank=True, max_length=250, null=True)),
     migrations.AddField(model_name=b'feedimage', name=b'thumbnail_url', field=models.CharField(blank=True, max_length=250, null=True))]