# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/event_logs/migrations/0003_auto_20180316_0005.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 623 bytes
import django.core.validators
from django.db import migrations, models
import re

class Migration(migrations.Migration):
    dependencies = [
     ('event_logs', '0002_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='eventlogcolor',
       name='rgb_color',
       field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator((re.compile('^\\d+(?:\\,\\d+)*\\Z', 32)), code='invalid', message='Enter only digits separated by commas.')]))]