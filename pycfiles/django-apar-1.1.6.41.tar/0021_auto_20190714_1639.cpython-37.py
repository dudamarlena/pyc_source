# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/educations/courses/migrations/0021_auto_20190714_1639.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 518 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('courses', '0020_auto_20190615_1430')]
    operations = [
     migrations.AlterField(model_name='coursesummary',
       name='type',
       field=models.CharField(choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس'), ('L', 'لینک')], max_length=1, verbose_name='نوع'))]