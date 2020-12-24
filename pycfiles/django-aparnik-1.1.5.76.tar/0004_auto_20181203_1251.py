# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/socials/migrations/0004_auto_20181203_1251.py
# Compiled at: 2018-12-03 04:27:40
from __future__ import unicode_literals
from django.db import migrations

def convert_to_new_structor(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    SocialNetwork = apps.get_model(b'socials', b'SocialNetwork')
    SocialNetwork2 = apps.get_model(b'socials', b'SocialNetwork2')
    for obj in SocialNetwork.objects.all():
        SocialNetwork2.objects.create(link=obj.link, icon=obj.icon, title=obj.title, android_app_shortcut=obj.android_app_shortcut, ios_app_shortcut=obj.ios_app_shortcut)
        obj.delete()


class Migration(migrations.Migration):
    dependencies = [
     ('socials', '0003_socialnetwork2')]
    operations = [
     migrations.RunPython(convert_to_new_structor, reverse_code=migrations.RunPython.noop)]