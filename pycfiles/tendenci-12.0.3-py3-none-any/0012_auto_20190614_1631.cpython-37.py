# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/events/migrations/0012_auto_20190614_1631.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 1259 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('events', '0011_auto_20190221_1402')]
    operations = [
     migrations.AddField(model_name='registration',
       name='gratuity',
       field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=6)),
     migrations.AddField(model_name='registrationconfiguration',
       name='gratuity_custom_option',
       field=models.BooleanField(default=False, verbose_name='Allow users to set their own gratuity')),
     migrations.AddField(model_name='registrationconfiguration',
       name='gratuity_enabled',
       field=models.BooleanField(default=False)),
     migrations.AddField(model_name='registrationconfiguration',
       name='gratuity_options',
       field=models.CharField(blank=True, default='17%,18%,19%,20%', help_text='Comma separated numeric numbers in percentage. A "%" will be appended if the percent sign is not present.', max_length=100, verbose_name='Gratuity Options'))]