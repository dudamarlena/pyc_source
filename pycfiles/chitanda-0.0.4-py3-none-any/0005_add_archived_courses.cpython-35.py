# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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