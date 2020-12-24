# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0007_auto_20160927_1706.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 399 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('corporate_memberships', '0006_auto_20160211_1542')]
    operations = [
     migrations.AddField(model_name='corpmembership',
       name='renew_from_id',
       field=models.IntegerField(null=True, blank=True))]