# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/news/migrations/0007_auto_20180315_1839.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 539 bytes
from django.db import migrations
import timezone_field.fields
from tendenci.apps.base.utils import get_timezone_choices

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0006_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='news',
       name='timezone',
       field=timezone_field.fields.TimeZoneField(choices=(get_timezone_choices()), verbose_name='Time Zone', default='US/Central', max_length=100))]