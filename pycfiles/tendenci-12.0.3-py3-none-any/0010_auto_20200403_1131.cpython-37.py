# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/memberships/migrations/0010_auto_20200403_1131.py
# Compiled at: 2020-04-03 15:09:22
# Size of source mod 2**32: 452 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('memberships', '0009_auto_20190725_1025')]
    operations = [
     migrations.AlterModelOptions(name='membershipapp',
       options={'permissions':(('view_app', 'Can view membership application'), ), 
      'verbose_name':'Membership Application'})]