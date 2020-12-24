# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Projects/django-basic-blog/blog/migrations/0003_auto_20141231_1242.py
# Compiled at: 2015-07-14 12:37:49
from __future__ import unicode_literals
from django.db import models, migrations
import django.utils.timezone, blog.fields

class Migration(migrations.Migration):
    dependencies = [
     ('blog', '0002_auto_20141231_0859')]
    operations = [
     migrations.AlterField(model_name=b'entry', name=b'created', field=models.DateTimeField(default=django.utils.timezone.now), preserve_default=True),
     migrations.AlterField(model_name=b'entry', name=b'modified', field=blog.fields.AutoDatetimeField(default=django.utils.timezone.now), preserve_default=True)]