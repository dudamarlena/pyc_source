# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/contactus/migrations/0002_auto_20181125_2227.py
# Compiled at: 2018-11-26 02:58:29
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('contactus', '0001_initial')]
    operations = [
     migrations.AlterField(model_name=b'contactus', name=b'content', field=models.TextField(blank=True, null=True, verbose_name=b'Content'))]