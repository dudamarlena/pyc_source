# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/migrations/0002_auto_20170425_0010.py
# Compiled at: 2019-04-03 22:56:30
# Size of source mod 2**32: 3541 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, filer.fields.file

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('core', '0001_initial'),
     ('filer', '0007_auto_20161016_1055'),
     ('vouchers', '0001_initial'),
     ('financial', '0001_initial'),
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.AddField(model_name='revenueitem',
       name='purchasedVoucher',
       field=models.OneToOneField(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='vouchers.Voucher', verbose_name='Purchased voucher/gift certificate')),
     migrations.AddField(model_name='revenueitem',
       name='registration',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='core.Registration')),
     migrations.AddField(model_name='revenueitem',
       name='submissionUser',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='revenuessubmittedby', to=(settings.AUTH_USER_MODEL))),
     migrations.AddField(model_name='expenseitem',
       name='attachment',
       field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='expense_attachment', to='filer.File', verbose_name='Attach File (optional)')),
     migrations.AddField(model_name='expenseitem',
       name='category',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='financial.ExpenseCategory')),
     migrations.AddField(model_name='expenseitem',
       name='event',
       field=models.ForeignKey(blank=True, help_text='If this item is associated with an Event, enter it here.', null=True, on_delete=(django.db.models.deletion.CASCADE), to='core.Event')),
     migrations.AddField(model_name='expenseitem',
       name='eventstaffmember',
       field=models.OneToOneField(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='core.EventStaffMember')),
     migrations.AddField(model_name='expenseitem',
       name='eventvenue',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='venueexpense', to='core.Event')),
     migrations.AddField(model_name='expenseitem',
       name='payToLocation',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='core.Location')),
     migrations.AddField(model_name='expenseitem',
       name='payToUser',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='payToUser', to=(settings.AUTH_USER_MODEL))),
     migrations.AddField(model_name='expenseitem',
       name='submissionUser',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), related_name='expensessubmittedby', to=(settings.AUTH_USER_MODEL)))]