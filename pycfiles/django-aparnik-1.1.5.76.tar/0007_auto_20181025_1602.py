# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0007_auto_20181025_1602.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations
from aparnik.utils.utils import convert_iran_phone_number_to_world_number

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0006_user_avatar')]

    def convert_username(apps, schema_editor):
        """
        We can't import the Post model directly as it may be a newer
        version than this migration expects. We use the historical version.
        """
        User = apps.get_model(b'aparnik_users', b'User')
        for user in User.objects.all():
            user.username = convert_iran_phone_number_to_world_number(user.username)
            user.save()

    operations = [
     migrations.RunPython(convert_username)]