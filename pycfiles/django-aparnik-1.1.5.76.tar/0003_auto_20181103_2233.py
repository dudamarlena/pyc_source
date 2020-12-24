# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/progresses/migrations/0003_auto_20181103_2233.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('progresses', '0002_progresssummary')]
    operations = [
     migrations.AlterField(model_name=b'progresses', name=b'file_obj', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'courses.CourseFile', verbose_name=b'File'))]