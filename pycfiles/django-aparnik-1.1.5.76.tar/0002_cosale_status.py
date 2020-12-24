# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/cosales/migrations/0002_cosale_status.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cosales', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'cosale', name=b'status', field=models.CharField(choices=[('C', 'Cleared'), ('NC', 'Not Cleared'), ('RSHBR', 'The request for settlement has been received')], default=b'NC', max_length=10, verbose_name=b'Status'))]