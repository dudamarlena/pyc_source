# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/discounts/migrations/0003_auto_20170724_2114.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 818 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('discounts', '0002_auto_20170717_1642')]
    operations = [
     migrations.AlterField(model_name='discountcombo',
       name='discountType',
       field=models.CharField(choices=[('F', 'Exact Specified Price'), ('D', 'Dollar Discount from Regular Price'), ('P', 'Percentage Discount from Regular Price'), ('A', 'Free Add-on Item (Can be combined with other discounts)')], default='D', help_text="Is this a flat price, a dollar amount discount, a 'percentage off' discount, or a free add-on?", max_length=1, verbose_name='Discount type'))]