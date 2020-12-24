# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0014_auto_20190214_1438.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 699 bytes
from django.db import migrations

def username_mention(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    User = apps.get_model('aparnik_users', 'User')
    for user in User.objects.all():
        user.username_mention = user.username
        user.save()


class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0013_user_username_mention')]
    operations = [
     migrations.RunPython(username_mention, reverse_code=(migrations.RunPython.noop))]