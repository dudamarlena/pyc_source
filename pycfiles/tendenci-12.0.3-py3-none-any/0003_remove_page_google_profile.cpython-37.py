# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/pages/migrations/0003_remove_page_google_profile.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 359 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0002_auto_20180315_0857')]
    operations = [
     migrations.RemoveField(model_name='page',
       name='google_profile')]