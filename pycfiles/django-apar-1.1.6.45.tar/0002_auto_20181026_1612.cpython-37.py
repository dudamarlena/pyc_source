# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/supports/migrations/0002_auto_20181026_1612.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 672 bytes
import aparnik.utils.fields, django.core.validators
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('supports', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='support',
       name='phone',
       field=aparnik.utils.fields.PhoneField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(code=b'nomatch', message='phone is not valid, please insert with code', regex=b'^0(?!0)\\d{2}([0-9]{8})$')], verbose_name='Phone'))]