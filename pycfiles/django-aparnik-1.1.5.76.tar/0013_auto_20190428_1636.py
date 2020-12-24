# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0013_auto_20190428_1636.py
# Compiled at: 2019-04-28 08:08:21
from __future__ import unicode_literals
from django.db import migrations

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    BaseCourse = apps.get_model(b'courses', b'BaseCourse')
    try:
        for course in BaseCourse.objects.all():
            course.content = course.description
            course.save()

    except Exception:
        pass


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    BaseCourse = apps.get_model(b'courses', b'BaseCourse')
    try:
        for course in BaseCourse.objects.all():
            course.description = course.content
            course.save()

    except Exception:
        pass


class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0012_basecourse_content')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]