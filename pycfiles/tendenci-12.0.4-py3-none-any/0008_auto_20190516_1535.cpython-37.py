# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/directories/migrations/0008_auto_20190516_1535.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 1205 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('directories', '0007_auto_20180315_1839')]
    operations = [
     migrations.AddField(model_name='directory',
       name='facebook',
       field=models.URLField(blank=True, default='', verbose_name='Facebook')),
     migrations.AddField(model_name='directory',
       name='instagram',
       field=models.URLField(blank=True, default='', verbose_name='Instagram')),
     migrations.AddField(model_name='directory',
       name='linkedin',
       field=models.URLField(blank=True, default='', verbose_name='LinkedIn')),
     migrations.AddField(model_name='directory',
       name='twitter',
       field=models.URLField(blank=True, default='', verbose_name='Twitter')),
     migrations.AddField(model_name='directory',
       name='youtube',
       field=models.URLField(blank=True, default='', verbose_name='YouTube'))]