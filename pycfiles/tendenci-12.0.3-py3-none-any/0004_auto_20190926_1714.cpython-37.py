# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/event_logs/migrations/0004_auto_20190926_1714.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 444 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('event_logs', '0003_auto_20180316_0005')]
    operations = [
     migrations.AlterField(model_name='eventlog',
       name='create_dt',
       field=models.DateTimeField(auto_now_add=True, db_index=True))]