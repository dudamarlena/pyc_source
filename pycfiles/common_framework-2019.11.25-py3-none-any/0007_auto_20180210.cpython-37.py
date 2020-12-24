# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0007_auto_20180210.py
# Compiled at: 2018-02-10 14:53:11
# Size of source mod 2**32: 769 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0006_auto_20170905')]
    operations = [
     migrations.AlterField(model_name='global',
       name='object_id',
       field=models.TextField(editable=False, verbose_name='identifiant')),
     migrations.AlterField(model_name='history',
       name='object_id',
       field=models.TextField(editable=False, verbose_name='identifiant')),
     migrations.AlterField(model_name='metadata',
       name='object_id',
       field=models.TextField(verbose_name='identifiant'))]