# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cristian/projects/python/django-qa/qa/migrations/0003_auto_20160414_1413.py
# Compiled at: 2018-03-17 13:09:30
# Size of source mod 2**32: 1437 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('qa', '0002_auto_20160412_1336')]
    operations = [
     migrations.AddField(model_name='answer',
       name='answer',
       field=models.BooleanField(default=False)),
     migrations.AlterField(model_name='answer',
       name='pub_date',
       field=models.DateTimeField(auto_now_add=True, verbose_name='date published')),
     migrations.AlterField(model_name='answercomment',
       name='pub_date',
       field=models.DateTimeField(auto_now_add=True, verbose_name='date published')),
     migrations.AlterField(model_name='question',
       name='pub_date',
       field=models.DateTimeField(auto_now_add=True, verbose_name='date published')),
     migrations.AlterField(model_name='questioncomment',
       name='pub_date',
       field=models.DateTimeField(auto_now_add=True, verbose_name='date published')),
     migrations.AlterField(model_name='userqaprofile',
       name='picture',
       field=models.ImageField(blank=True, upload_to='qa/static/profile_images'))]