# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/socials/migrations/0005_socialnetwork_value.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('socials', '0004_auto_20181203_1328')]
    operations = [
     migrations.AddField(model_name=b'socialnetwork', name=b'value', field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Value'))]