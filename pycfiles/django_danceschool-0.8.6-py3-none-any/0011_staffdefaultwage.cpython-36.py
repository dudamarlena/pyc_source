# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0011_staffdefaultwage.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 1473 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0025_auto_20181109_1631'),
     ('financial', '0010_auto_20181109_1854')]
    operations = [
     migrations.CreateModel(name='StaffDefaultWage',
       fields=[
      (
       'repeatedexpenserule_ptr', models.OneToOneField(auto_created=True, on_delete=(django.db.models.deletion.CASCADE), parent_link=True, primary_key=True, serialize=False, to='financial.RepeatedExpenseRule')),
      (
       'category', models.OneToOneField(help_text='If left blank, then this expense rule will be used for all categories.  If a category-specific rate is specified, then that will be used instead.  If nothing is specified for a staff member, then the default hourly rate for each category will be used.', on_delete=(django.db.models.deletion.CASCADE), related_name='defaultwage', to='core.EventStaffCategory', verbose_name='Category'))],
       options={'verbose_name':'Default staff wage', 
      'verbose_name_plural':'Default staff wages', 
      'ordering':('category__name', ), 
      'manager_inheritance_from_future':True},
       bases=('financial.repeatedexpenserule', ))]