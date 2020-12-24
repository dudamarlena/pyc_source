# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cristian/projects/python/django-qa/qa/migrations/0005_auto_20160519_1057.py
# Compiled at: 2018-03-17 13:09:30
# Size of source mod 2**32: 876 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('qa', '0004_answer_updated')]
    operations = [
     migrations.AddField(model_name='answer',
       name='negative_votes',
       field=models.IntegerField(default=0)),
     migrations.AddField(model_name='answer',
       name='positive_votes',
       field=models.IntegerField(default=0)),
     migrations.AddField(model_name='question',
       name='negative_votes',
       field=models.IntegerField(default=0)),
     migrations.AddField(model_name='question',
       name='positive_votes',
       field=models.IntegerField(default=0))]