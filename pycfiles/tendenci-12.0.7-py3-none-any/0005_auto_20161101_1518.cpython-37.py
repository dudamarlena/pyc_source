# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/migrations/0005_auto_20161101_1518.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 879 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('memberships', '0004_auto_20160520_1740')]
    operations = [
     migrations.AddField(model_name='membershipapp',
       name='donation_default_amount',
       field=models.DecimalField(default=0, verbose_name='Default Amount', max_digits=15, decimal_places=2, blank=True)),
     migrations.AddField(model_name='membershipapp',
       name='donation_enabled',
       field=models.BooleanField(default=False, verbose_name='Enable Donation')),
     migrations.AddField(model_name='membershipapp',
       name='donation_label',
       field=models.CharField(max_length=255, null=True, verbose_name='Label', blank=True))]