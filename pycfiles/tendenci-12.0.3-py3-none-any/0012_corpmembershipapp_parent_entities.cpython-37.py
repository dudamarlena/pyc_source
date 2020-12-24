# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/corporate_memberships/migrations/0012_corpmembershipapp_parent_entities.py
# Compiled at: 2020-03-30 17:48:03
# Size of source mod 2**32: 546 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('entities', '0001_initial'),
     ('corporate_memberships', '0011_auto_20171201_1726')]
    operations = [
     migrations.AddField(model_name='corpmembershipapp',
       name='parent_entities',
       field=models.ManyToManyField(help_text='Specify a list of parent entities to select.', to='entities.Entity', verbose_name='Parent Entities', blank=True))]