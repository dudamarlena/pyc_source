# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course/migrations/0040_auto_20180624_1439.py
# Compiled at: 2018-06-26 00:36:23
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course', '0039_auto_20180622_1445')]
    operations = [
     migrations.AddField(model_name=b'usersectionnote', name=b'is_digest', field=models.BooleanField(default=False, verbose_name=b'是否精华')),
     migrations.AddField(model_name=b'usersectionnote', name=b'is_stick', field=models.BooleanField(default=False, verbose_name=b'是否置顶'))]