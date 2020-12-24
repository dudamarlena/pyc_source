# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /libs/django_brfied/django_brfied/migrations/0002_auto_20190227_2335.py
# Compiled at: 2019-02-27 18:35:25
# Size of source mod 2**32: 518 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_brfied', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='unidadefederativa',
       name='regiao',
       field=models.CharField(choices=[('N', 'Norte'), ('NE', 'Nordeste'), ('SE', 'Sudeste'), ('S', 'Sul'), ('CO', 'Centro-oeste')], max_length=2, verbose_name='Região'))]