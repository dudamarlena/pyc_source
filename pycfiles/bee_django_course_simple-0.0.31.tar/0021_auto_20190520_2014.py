# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0021_auto_20190520_2014.py
# Compiled at: 2019-05-20 08:14:54
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0020_auto_20190515_1427')]
    operations = [
     migrations.AddField(model_name=b'section', name=b'auto_pass', field=models.BooleanField(default=False, verbose_name=b'自动通过')),
     migrations.AddField(model_name=b'section', name=b'type', field=models.IntegerField(choices=[(1, '普通课件'), (2, '预备课件')], default=1, verbose_name=b'课件类型'))]