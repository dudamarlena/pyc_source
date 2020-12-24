# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0007_max_length_by_integer.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 433 bytes
from django.db import models, migrations

class Migration(migrations.Migration):
    dependencies = [
     ('helpdesk', '0006_email_maxlength')]
    operations = [
     migrations.AlterField(model_name='customfield',
       name='label',
       field=models.CharField(help_text='The display label for this field', max_length=30, verbose_name='Label'))]