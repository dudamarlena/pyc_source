# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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