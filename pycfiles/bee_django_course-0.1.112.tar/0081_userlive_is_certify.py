# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0081_userlive_is_certify.py
# Compiled at: 2019-12-27 05:06:18
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0080_auto_20191227_1525')]
    operations = [
     migrations.AddField(model_name=b'userlive', name=b'is_certify', field=models.BooleanField(default=False))]