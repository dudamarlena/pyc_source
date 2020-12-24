# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0005_add_archived_courses.py
# Compiled at: 2017-09-19 13:56:43
# Size of source mod 2**32: 455 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0004_validate_extensions_used')]
    operations = [
     migrations.AddField(model_name='course', name='archived', field=models.BooleanField(default=False))]