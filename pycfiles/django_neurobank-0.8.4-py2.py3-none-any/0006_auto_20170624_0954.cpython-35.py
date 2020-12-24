# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0006_auto_20170624_0954.py
# Compiled at: 2017-06-24 09:54:47
# Size of source mod 2**32: 662 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0005_auto_20170624_0943')]
    operations = [
     migrations.AlterField(model_name='datatype', name='name', field=models.CharField(max_length=32, unique=True)),
     migrations.AlterField(model_name='domain', name='name', field=models.CharField(help_text='A descriptive name', max_length=32, unique=True))]