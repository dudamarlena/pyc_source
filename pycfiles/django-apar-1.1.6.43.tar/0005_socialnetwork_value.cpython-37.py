# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/socials/migrations/0005_socialnetwork_value.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 462 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('socials', '0004_auto_20181203_1328')]
    operations = [
     migrations.AddField(model_name='socialnetwork',
       name='value',
       field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Value'))]