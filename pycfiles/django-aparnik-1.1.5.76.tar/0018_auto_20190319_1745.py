# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0018_auto_20190319_1745.py
# Compiled at: 2019-03-19 10:16:52
from __future__ import unicode_literals
from django.db import migrations
from faker import Faker

def username_mention(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    faker = Faker()
    User = apps.get_model(b'aparnik_users', b'User')
    for user in User.objects.all():
        username = faker.user_name()
        while User.objects.filter(username_mention=username).exists():
            username = faker.user_name()

        user.username_mention = username
        user.save()


class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0017_auto_20190319_1744')]
    operations = [
     migrations.RunPython(username_mention, reverse_code=migrations.RunPython.noop)]