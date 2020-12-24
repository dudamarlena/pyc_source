# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/migrations/0007_membershipdefault_auto_renew.py
# Compiled at: 2020-04-03 15:08:31
# Size of source mod 2**32: 406 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('memberships', '0006_membershipset_donation_amount')]
    operations = [
     migrations.AddField(model_name='membershipdefault',
       name='auto_renew',
       field=models.BooleanField(blank=True, default=False))]