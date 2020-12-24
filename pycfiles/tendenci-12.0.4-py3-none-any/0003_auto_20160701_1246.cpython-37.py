# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/news/migrations/0003_auto_20160701_1246.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 537 bytes
from django.db import migrations, models
import tendenci.apps.user_groups.utils

class Migration(migrations.Migration):
    dependencies = [
     ('user_groups', '0001_initial'),
     ('news', '0002_auto_20150804_1545')]
    operations = [
     migrations.AddField(model_name='news',
       name='groups',
       field=models.ManyToManyField(default=(tendenci.apps.user_groups.utils.get_default_group), related_name='group_news', to='user_groups.Group'))]