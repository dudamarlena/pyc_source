# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/discounts/migrations/0004_auto_20170808_2020.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 1006 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('discounts', '0003_auto_20170724_2114')]
    operations = [
     migrations.AddField(model_name='discountcombo',
       name='daysInAdvanceRequired',
       field=models.PositiveIntegerField(blank=True, help_text='For this discount to apply, all components must be satisfied by events that begin this many days in the future (measured from midnight of the date of registration).  Leave blank for no restriction.', null=True, verbose_name='Must register __ days in advance')),
     migrations.AddField(model_name='discountcombo',
       name='expirationDate',
       field=models.DateTimeField(blank=True, help_text='Leave blank for no expiration.', null=True, verbose_name='Expiration Date'))]