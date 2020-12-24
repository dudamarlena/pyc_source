# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/huangwei/code/bee_apps_site/bee_django_social_feed/migrations/0006_auto_20180701_0938.py
# Compiled at: 2018-06-30 21:38:24
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_social_feed', '0005_albumphoto')]
    operations = [
     migrations.AlterModelOptions(name=b'albumphoto', options={b'ordering': [b'-created_at']})]