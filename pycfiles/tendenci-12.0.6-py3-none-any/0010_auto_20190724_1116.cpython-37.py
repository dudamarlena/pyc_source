# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/helpdesk/migrations/0010_auto_20190724_1116.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 625 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('helpdesk', '0009_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='ticket',
       name='assigned_to',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), related_name='assigned_to', to=(settings.AUTH_USER_MODEL), verbose_name='Assigned to'))]