# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0003_auto_20151120_1531.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 764 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0002_auto_20150804_1545')]
    operations = [
     migrations.AddField(model_name='corporatemembershiptype',
       name='apply_cap',
       field=models.BooleanField(default=False, help_text='If checked, specify the membership cap below.', verbose_name='Apply cap')),
     migrations.AddField(model_name='corporatemembershiptype',
       name='membership_cap',
       field=models.IntegerField(default=0, help_text='The maximum number of employees allowed.', null=True, verbose_name='Membership cap', blank=True))]