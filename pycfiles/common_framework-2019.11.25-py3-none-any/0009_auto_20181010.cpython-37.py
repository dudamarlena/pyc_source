# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/migrations/0009_auto_20181010.py
# Compiled at: 2018-10-10 19:41:58
# Size of source mod 2**32: 780 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('common', '0008_auto_20180302')]
    operations = [
     migrations.AddField(model_name='serviceusage',
       name='reset',
       field=models.CharField(choices=[('H', 'Toutes les heures'), ('D', 'Tous les jours'), ('W', 'Toutes les semaines'), ('M', 'Tous les mois'), ('Y', 'Tous les ans')], blank=True, max_length=1, verbose_name='réinitialisation')),
     migrations.AddField(model_name='serviceusage',
       name='reset_date',
       field=models.DateTimeField(blank=True, null=True, verbose_name='date réinitialisation'))]