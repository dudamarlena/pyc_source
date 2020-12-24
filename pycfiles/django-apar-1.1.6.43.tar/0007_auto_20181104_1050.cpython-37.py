# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0007_auto_20181104_1050.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 707 bytes
from django.db import migrations
import datetime

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0006_coursefile_seconds')]

    def convert_to_seconds(apps, schema_editor):
        Object = apps.get_model('courses', 'CourseFile')
        for obj in Object.objects.all():
            obj.seconds = datetime.timedelta(hours=(obj.time.hour), minutes=(obj.time.minute), seconds=(obj.time.second)).total_seconds()
            obj.save()

    operations = [
     migrations.RunPython(convert_to_seconds, reverse_code=(migrations.RunPython.noop))]