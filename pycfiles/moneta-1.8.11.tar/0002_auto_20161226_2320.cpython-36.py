# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/migrations/0002_auto_20161226_2320.py
# Compiled at: 2017-07-28 01:43:32
# Size of source mod 2**32: 448 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('repository', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='repository',
       name='on_index',
       field=models.BooleanField(db_index=True, default=True, verbose_name="Afficher sur l'index public ?"))]