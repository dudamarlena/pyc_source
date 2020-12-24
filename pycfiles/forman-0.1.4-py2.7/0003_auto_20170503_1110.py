# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/migrations/0003_auto_20170503_1110.py
# Compiled at: 2017-05-08 12:16:33
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('forman', '0002_auto_20170502_1406')]
    operations = [
     migrations.AlterField(model_name=b'input', name=b'display_type', field=models.CharField(choices=[('text', 'text'), ('image', 'image'), ('password', 'password'), ('radio', 'radio'), ('submit', 'submit'), ('reset', 'reset'), ('textarea', 'textarea'), ('file', 'file'), ('select', 'select'), ('multi-select', 'multi-select'), ('checkbox', 'checkbox')], max_length=100))]