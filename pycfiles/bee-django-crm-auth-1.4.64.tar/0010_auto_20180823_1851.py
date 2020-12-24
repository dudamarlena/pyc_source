# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0010_auto_20180823_1851.py
# Compiled at: 2018-08-23 06:51:10
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0009_applicationquestion_is_required')]
    operations = [
     migrations.AlterField(model_name=b'applicationquestion', name=b'is_required', field=models.BooleanField(default=False, help_text=b'只对输入框和单选有效', verbose_name=b'是否必填'))]