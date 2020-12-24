# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0016_auto_20190428_1646.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1151 bytes
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    BaseCourse = apps.get_model('courses', 'BaseCourse')
    try:
        for course in BaseCourse.objects.all():
            course.description = course.content
            course.save()

    except Exception:
        pass


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    BaseCourse = apps.get_model('courses', 'BaseCourse')
    try:
        for course in BaseCourse.objects.all():
            course.content = course.description
            course.save()

    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0015_basecourse_description')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]