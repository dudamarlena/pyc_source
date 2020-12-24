# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/events/migrations/0011_auto_20190221_1402.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 790 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('events', '0010_addon_default_yes')]
    operations = [
     migrations.AddField(model_name='regconfpricing',
       name='registration_cap',
       field=models.IntegerField(default=0, help_text='The maximum number of registrants allowed for this pricing. 0 indicates unlimited. Note: this number should not exceed the specified registration limit.', verbose_name='Registration limit')),
     migrations.AddField(model_name='regconfpricing',
       name='spots_taken',
       field=models.IntegerField(default=0))]