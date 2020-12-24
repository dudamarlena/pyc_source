# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0008_auto_20170803_2038.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 503 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0001_initial'),
     ('corporate_memberships', '0007_auto_20160927_1706')]
    operations = [
     migrations.AddField(model_name='corpprofile',
       name='logo',
       field=models.ForeignKey(to='files.File', null=True, on_delete=(django.db.models.deletion.CASCADE)))]