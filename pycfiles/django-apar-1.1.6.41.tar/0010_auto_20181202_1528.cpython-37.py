# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0010_auto_20181202_1528.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 980 bytes
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0009_user_co_sale_percentage_value')]
    operations = [
     migrations.AlterField(model_name='user',
       name='co_sale_percentage_value',
       field=models.IntegerField(default=(-1), help_text='If the number is set to -1, then the value in the settings will apply', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(-1)], verbose_name='Co Sale Percentage')),
     migrations.AlterField(model_name='user',
       name='limit_device_login',
       field=models.IntegerField(default=(-1), help_text='If the number is set to -1, then the value in the settings will apply', verbose_name='Limit device login'))]