# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/migrations/0005_auto_20170503_1526.py
# Compiled at: 2017-05-08 12:16:33
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('forman', '0004_sumission')]
    operations = [
     migrations.RenameModel(old_name=b'Sumission', new_name=b'Submission')]