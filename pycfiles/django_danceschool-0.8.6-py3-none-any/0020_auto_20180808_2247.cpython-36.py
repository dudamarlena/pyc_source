# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0020_auto_20180808_2247.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 1240 bytes
from __future__ import unicode_literals
import danceschool.core.mixins
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0019_invoice_buyerpayssalestax')]
    operations = [
     migrations.CreateModel(name='CustomerGroup',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100, verbose_name='Group name'))],
       options={'ordering':('name', ), 
      'verbose_name':'Customer group', 
      'verbose_name_plural':'Customer groups'},
       bases=(
      danceschool.core.mixins.EmailRecipientMixin, models.Model)),
     migrations.AddField(model_name='customer',
       name='groups',
       field=models.ManyToManyField(blank=True, help_text='Customer groups may be used for group-specific discounts and vouchers, as well as for email purposes.', to='core.CustomerGroup', verbose_name='Customer groups'))]