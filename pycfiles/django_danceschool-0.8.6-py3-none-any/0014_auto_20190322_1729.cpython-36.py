# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0014_auto_20190322_1729.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 883 bytes
from __future__ import unicode_literals
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('financial', '0013_auto_20181219_2044')]
    operations = [
     migrations.AlterModelOptions(name='revenueitem',
       options={'ordering':[
       '-accrualDate'], 
      'permissions':(('mark_revenues_received', 'Mark revenues as received at the time of submission'),
 ('export_financial_data', 'Export detailed financial transaction information to CSV'),
 ('view_finances_bymonth', 'View school finances month-by-month'), ('view_finances_byevent', 'View school finances by Event'),
 ('view_finances_detail', 'View school finances as detailed statement')),  'verbose_name':'Revenue item',  'verbose_name_plural':'Revenue items'})]