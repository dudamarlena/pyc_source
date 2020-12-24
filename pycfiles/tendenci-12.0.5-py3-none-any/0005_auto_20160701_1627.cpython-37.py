# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/news/migrations/0005_auto_20160701_1627.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 299 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0004_auto_20160701_1247')]
    operations = [
     migrations.RemoveField(model_name='news',
       name='group')]