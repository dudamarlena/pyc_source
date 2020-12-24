# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_accounts_light/migrations/0003_auto_20181119_2119.py
# Compiled at: 2018-11-19 16:19:26
# Size of source mod 2**32: 417 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ohm2_accounts_light', '0002_auto_20181119_2052')]
    operations = [
     migrations.AlterField(model_name='passwordreset', name='code', field=models.CharField(max_length=255, unique=True))]