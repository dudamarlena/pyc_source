# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/payments/stripe/migrations/0002_auto_20180508_1659.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 949 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('stripe', '0001_initial')]
    operations = [
     migrations.RemoveField(model_name='stripeaccount',
       name='livemode_access_token'),
     migrations.RemoveField(model_name='stripeaccount',
       name='livemode_stripe_publishable_key'),
     migrations.RemoveField(model_name='stripeaccount',
       name='refresh_token'),
     migrations.RemoveField(model_name='stripeaccount',
       name='testmode_access_token'),
     migrations.RemoveField(model_name='stripeaccount',
       name='testmode_stripe_publishable_key'),
     migrations.RemoveField(model_name='stripeaccount',
       name='token_type')]