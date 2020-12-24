# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0002_expensedetail_entry.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1392 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from lucterios.framework.tools import set_locale_lang
from lucterios.CORE.models import PrintModel

def printer_model(*args):
    set_locale_lang(settings.LANGUAGE_CODE)
    PrintModel().load_model('diacamma.condominium', 'Owner_0001', is_default=True)


class Migration(migrations.Migration):
    dependencies = [
     ('accounting', '0002_add_param'),
     ('condominium', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='expense', options={'ordering': [
                   '-date'], 
      'verbose_name': 'expense', 'verbose_name_plural': 'expenses'}),
     migrations.AddField(model_name='expensedetail', name='entry', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounting.EntryAccount', verbose_name='entry')),
     migrations.AddField(model_name='owner', name='information', field=models.CharField(default='', max_length=200, null=True, verbose_name='information')),
     migrations.RunPython(printer_model)]