# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_pushes_light/gateways/onesignal/migrations/0002_auto_20180928_1418.py
# Compiled at: 2018-09-28 10:18:29
# Size of source mod 2**32: 534 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('onesignal', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='device', name='user', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='onesignal_device', to=settings.AUTH_USER_MODEL))]