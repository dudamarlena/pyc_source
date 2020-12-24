# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_crm/migrations/0005_auto_20180708_1503.py
# Compiled at: 2018-07-08 03:03:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_crm', '0004_auto_20180622_1603')]
    operations = [
     migrations.AlterField(model_name=b'poster', name=b'photo', field=models.ImageField(null=True, upload_to=b'bee_django_crm/poster_photo'))]