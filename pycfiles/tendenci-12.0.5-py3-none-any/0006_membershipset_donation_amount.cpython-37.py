# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/migrations/0006_membershipset_donation_amount.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 425 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('memberships', '0005_auto_20161101_1518')]
    operations = [
     migrations.AddField(model_name='membershipset',
       name='donation_amount',
       field=models.DecimalField(default=0, max_digits=15, decimal_places=2, blank=True))]