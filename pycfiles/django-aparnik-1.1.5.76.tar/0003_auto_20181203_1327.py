# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/socials/migrations/0003_auto_20181203_1327.py
# Compiled at: 2018-12-03 11:15:34
from __future__ import unicode_literals
from django.db import migrations

def empty_table(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    SocialNetwork = apps.get_model(b'socials', b'SocialNetwork')
    SocialNetwork.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
     ('socials', '0002_socialnetworksegment')]
    operations = [
     migrations.RunPython(empty_table, reverse_code=migrations.RunPython.noop)]