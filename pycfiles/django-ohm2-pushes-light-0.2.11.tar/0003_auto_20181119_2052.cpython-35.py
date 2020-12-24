# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_pushes_light/gateways/onesignal/migrations/0003_auto_20181119_2052.py
# Compiled at: 2018-11-19 15:52:54
# Size of source mod 2**32: 404 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('onesignal', '0002_auto_20180928_1418')]
    operations = [
     migrations.AlterField(model_name='device', name='identity', field=models.CharField(max_length=255, unique=True))]