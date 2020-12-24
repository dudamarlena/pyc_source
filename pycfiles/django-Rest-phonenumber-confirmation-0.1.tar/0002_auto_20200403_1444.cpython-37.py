# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/migrations/0002_auto_20200403_1444.py
# Compiled at: 2020-04-03 10:44:19
# Size of source mod 2**32: 516 bytes
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('phonenumber_confirmation', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='phonenumberconfirmation',
       name='pin',
       field=models.IntegerField(unique=True, validators=[django.core.validators.MaxLengthValidator(6)], verbose_name='pin'))]