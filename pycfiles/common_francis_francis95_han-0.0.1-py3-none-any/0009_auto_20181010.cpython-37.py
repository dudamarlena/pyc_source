# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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