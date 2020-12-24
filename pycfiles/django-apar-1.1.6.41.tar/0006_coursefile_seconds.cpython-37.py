# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0006_coursefile_seconds.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 477 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0005_remove_course_is_free')]
    operations = [
     migrations.AddField(model_name='coursefile',
       name='seconds',
       field=models.CharField(default='0', max_length=255, verbose_name='\\u0632\\u0645\\u0627\\u0646'))]