# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/migrations/0003_asyncprocess_process_type.py
# Compiled at: 2019-09-30 06:45:25
# Size of source mod 2**32: 424 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('tom_education', '0002_observationalert')]
    operations = [
     migrations.AddField(model_name='asyncprocess',
       name='process_type',
       field=models.CharField(blank=True, max_length=100, null=True))]