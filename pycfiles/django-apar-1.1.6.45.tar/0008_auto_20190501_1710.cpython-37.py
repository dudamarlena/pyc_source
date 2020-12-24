# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0008_auto_20190501_1710.py
# Compiled at: 2020-03-03 06:09:02
# Size of source mod 2**32: 1308 bytes
from django.db import migrations
from aparnik.utils.utils import is_app_installed

def add_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    try:
        CourseFile = apps.get_model('courses', 'CourseFile')
        for course_file in CourseFile.objects.all():
            course_file.file_obj.seconds = course_file.seconds
            course_file.file_obj.save()

    except:
        return


def remove_keys(apps, schema_editor):
    """
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    """
    try:
        CourseFile = apps.get_model('courses', 'CourseFile')
        for course_file in CourseFile.objects.all():
            course_file.seconds = course_file.file_obj.seconds
            course_file.save()

    except:
        return


class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0007_filefield_seconds')]
    operations = [
     migrations.RunPython(add_keys, reverse_code=remove_keys)]