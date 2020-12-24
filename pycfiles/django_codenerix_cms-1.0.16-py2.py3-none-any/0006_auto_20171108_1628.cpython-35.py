# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/migrations/0006_auto_20171108_1628.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 559 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_cms', '0005_auto_20170517_1046')]
    operations = [
     migrations.AlterField(model_name='staticpage', name='status', field=models.CharField(choices=[('D', 'Draft'), ('R', 'Public'), ('P', 'Pending')], default='D', max_length=150, verbose_name='Status'))]