# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Projects/django-basic-blog/blog/migrations/0002_auto_20141231_0859.py
# Compiled at: 2015-07-14 12:37:49
from __future__ import unicode_literals
from django.db import models, migrations
import datetime, blog.fields

class Migration(migrations.Migration):
    dependencies = [
     ('blog', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'entry', options={b'verbose_name_plural': b'entries'}),
     migrations.AddField(model_name=b'entry', name=b'created', field=models.DateTimeField(default=datetime.datetime.now), preserve_default=True),
     migrations.AddField(model_name=b'entry', name=b'modified', field=blog.fields.AutoDatetimeField(default=datetime.datetime.now), preserve_default=True)]