# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/migrations/0009_taxreceipt.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 1801 bytes
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from lucterios.framework.tools import set_locale_lang
from lucterios.CORE.models import PrintModel

def initial_values(*args):
    set_locale_lang(settings.LANGUAGE_CODE)
    PrintModel().load_model('diacamma.member', 'TaxReceipt_0001', is_default=True)


class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0007_bankaccount'),
     ('accounting', '0013_fiscalyear_folder'),
     ('member', '0008_thirdadherent')]
    operations = [
     migrations.CreateModel(name='TaxReceipt', fields=[
      (
       'supporting_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payoff.Supporting')),
      (
       'num', models.IntegerField(null=False, verbose_name='numeros')),
      (
       'entries', models.ManyToManyField(to='accounting.EntryAccount', verbose_name='entries')),
      (
       'fiscal_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.FiscalYear', verbose_name='fiscal year')),
      (
       'year', models.IntegerField(null=False, verbose_name='year', unique_for_year=True)),
      (
       'date', models.DateField(verbose_name='date', null=False))], options={'verbose_name': 'tax receipt', 
      'verbose_name_plural': 'tax receipts', 
      'ordering': ['year', 'num', 'third'], 
      'default_permissions': ['change']}, bases=('payoff.supporting', )),
     migrations.RunPython(initial_values)]