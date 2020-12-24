# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0009_auto_20171204_1700.py
# Compiled at: 2018-03-26 19:55:30
# Size of source mod 2**32: 894 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('financial', '0008_revenueitem_buyerpayssalestax')]
    operations = [
     migrations.AddField(model_name='repeatedexpenserule', name='advanceDaysReference', field=models.CharField(choices=[('S', 'First occurrence starts'), ('E', 'Last occurrence ends')], default='S', max_length=1, verbose_name='in advance of')),
     migrations.AddField(model_name='repeatedexpenserule', name='priorDaysReference', field=models.CharField(choices=[('S', 'First occurrence starts'), ('E', 'Last occurrence ends')], default='E', max_length=1, verbose_name='prior to'))]