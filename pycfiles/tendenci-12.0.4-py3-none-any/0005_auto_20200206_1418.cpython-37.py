# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/event_logs/migrations/0005_auto_20200206_1418.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 622 bytes
import django.core.validators
from django.db import migrations, models
import re

class Migration(migrations.Migration):
    dependencies = [
     ('event_logs', '0004_auto_20190926_1714')]
    operations = [
     migrations.AlterField(model_name='eventlogcolor',
       name='rgb_color',
       field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator((re.compile('^\\d+(?:,\\d+)*\\Z', 32)), code='invalid', message='Enter only digits separated by commas.')]))]