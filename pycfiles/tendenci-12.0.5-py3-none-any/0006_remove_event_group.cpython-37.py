# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/events/migrations/0006_remove_event_group.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 302 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('events', '0005_auto_20160603_1347')]
    operations = [
     migrations.RemoveField(model_name='event',
       name='group')]