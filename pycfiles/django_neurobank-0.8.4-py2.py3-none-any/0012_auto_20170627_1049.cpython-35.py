# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmeliza/Devel/django-neurobank/neurobank/migrations/0012_auto_20170627_1049.py
# Compiled at: 2017-06-27 10:49:51
# Size of source mod 2**32: 851 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('neurobank', '0011_auto_20170626_1616')]
    operations = [
     migrations.AlterField(model_name='datatype', name='name', field=models.SlugField(max_length=32, unique=True)),
     migrations.AlterField(model_name='domain', name='name', field=models.SlugField(help_text='a descriptive name', max_length=32, unique=True)),
     migrations.AlterField(model_name='domain', name='root', field=models.CharField(help_text='root path for resources', max_length=512))]