# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/migrations/0009_gradescope.py
# Compiled at: 2020-01-15 11:47:40
# Size of source mod 2**32: 920 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('api', '0008_python3+django2_upgrade')]
    operations = [
     migrations.AddField(model_name='assignment', name='expected_files', field=models.TextField(blank=True, null=True)),
     migrations.AddField(model_name='assignment', name='gradescope_id', field=models.IntegerField(blank=True, null=True)),
     migrations.AddField(model_name='course', name='gradescope_id', field=models.IntegerField(blank=True, null=True)),
     migrations.AddField(model_name='registration', name='gradescope_uploaded', field=models.BooleanField(default=False))]