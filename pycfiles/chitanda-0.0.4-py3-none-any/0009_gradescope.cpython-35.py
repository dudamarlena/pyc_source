# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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