# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0012_remove_grade_cert_image.py
# Compiled at: 2018-01-19 02:20:07
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0011_auto_20180118_1719')]
    operations = [
     migrations.RemoveField(model_name=b'grade', name=b'cert_image')]