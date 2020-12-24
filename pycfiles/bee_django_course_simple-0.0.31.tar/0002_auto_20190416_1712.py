# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_course_simple/migrations/0002_auto_20190416_1712.py
# Compiled at: 2019-04-16 05:12:20
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_course_simple', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'option', options={b'ordering': [b'number']}),
     migrations.AlterModelOptions(name=b'part', options={b'ordering': [b'number'], b'verbose_name': b'小节'}),
     migrations.AlterModelOptions(name=b'question', options={b'ordering': [b'number']}),
     migrations.AlterModelOptions(name=b'section', options={b'ordering': [b'number'], b'verbose_name': b'course课件'}),
     migrations.AlterModelOptions(name=b'video', options={b'ordering': [b'number']})]