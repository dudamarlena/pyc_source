# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forms_builder/forms/migrations/0005_auto_20191219_1249.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 949 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('forms', '0004_auto_20180315_0857')]
    operations = [
     migrations.AlterField(model_name='field',
       name='field_function',
       field=models.CharField(blank=True, choices=[('GroupSubscription', 'Subscribe to Group'), ('GroupSubscriptionAuto', 'Subscribe to Group (Auto)'), ('EmailFirstName', 'First Name'), ('EmailLastName', 'Last Name'), ('EmailFullName', 'Full Name'), ('EmailPhoneNumber', 'Phone Number'), ('Recipients', 'Email to Recipients'), ('company', 'Company'), ('address', 'Address'), ('city', 'City'), ('state', 'State'), ('zipcode', 'Zip'), ('position_title', 'Position Title'), ('referral_source', 'Referral Source')], max_length=64, null=True, verbose_name='Special Functionality'))]