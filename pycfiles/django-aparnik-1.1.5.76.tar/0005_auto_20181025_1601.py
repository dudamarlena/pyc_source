# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/users/migrations/0005_auto_20181025_1601.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
import aparnik.utils.fields, django.core.validators
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('aparnik_users', '0004_auto_20180814_0159')]
    operations = [
     migrations.RemoveField(model_name=b'user', name=b'avatar'),
     migrations.AlterField(model_name=b'user', name=b'username', field=aparnik.utils.fields.PhoneField(max_length=30, unique=True, validators=[
      django.core.validators.RegexValidator(code=b'nomatch', message=b'phone is not valid, please insert with code', regex=b'^0(?!0)\\d{2}([0-9]{8})$')], verbose_name=b'Mobile')),
     migrations.AddField(model_name=b'user', name=b'wallet', field=aparnik.utils.fields.PriceField(decimal_places=0, default=0, max_digits=20, verbose_name=b'Wallet'))]