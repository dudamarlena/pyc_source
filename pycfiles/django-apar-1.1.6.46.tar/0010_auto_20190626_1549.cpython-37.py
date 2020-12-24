# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/reviews/migrations/0010_auto_20190626_1549.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1019 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Review = apps.get_model('reviews', 'Review')
    for obj in Review.objects.all():
        obj.user_obj_2 = obj.user_obj
        obj.save()


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    Review = apps.get_model('reviews', 'Review')
    for obj in Review.objects.all():
        obj.user_obj = obj.user_obj_2
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
     ('reviews', '0009_review_user_obj_2')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]