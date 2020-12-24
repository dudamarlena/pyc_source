# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0006_auto_20160211_1542.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 819 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0005_auto_20151120_1552')]
    operations = [
     migrations.AddField(model_name='corporatemembershiptype',
       name='above_cap_price',
       field=models.DecimalField(decimal_places=2, default=0, max_digits=15, blank=True, help_text='Price for members who join above cap.', null=True, verbose_name='Membership cap')),
     migrations.AddField(model_name='corporatemembershiptype',
       name='allow_above_cap',
       field=models.BooleanField(default=False, help_text='Check this box to allow additional member join above cap.', verbose_name='Allow above cap'))]