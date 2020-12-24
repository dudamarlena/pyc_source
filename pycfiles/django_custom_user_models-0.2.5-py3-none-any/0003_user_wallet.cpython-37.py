# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0003_user_wallet.py
# Compiled at: 2019-12-11 09:45:43
# Size of source mod 2**32: 445 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0002_date_joined_auto_now_add')]
    operations = [
     migrations.AddField(model_name='user',
       name='wallet',
       field=models.PositiveIntegerField(default=0, verbose_name='Credit of user'))]