# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\migrations\0008_auto_20200128_2201.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 537 bytes
from django.db import migrations
import phonenumber_field.modelfields

class Migration(migrations.Migration):
    dependencies = [
     ('CustomAuth', '0007_phonenumberuser')]
    operations = [
     migrations.AlterField(model_name='phonenumberuser',
       name='cellphone',
       field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IR', unique=True, verbose_name='تلفن همراه'))]