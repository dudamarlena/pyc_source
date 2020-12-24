# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0016_recoverableloadratio.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1418 bytes
import django.core.validators
from django.conf import settings
from django.db import migrations, models
from lucterios.framework.tools import set_locale_lang
from lucterios.CORE.models import PrintModel

def printer_model(*_args):
    set_locale_lang(settings.LANGUAGE_CODE)
    PrintModel().load_model('diacamma.condominium', 'Owner_0003', is_default=False)


class Migration(migrations.Migration):
    dependencies = [
     ('payoff', '0007_bankaccount'),
     ('condominium', '0015_calldetail')]
    operations = [
     migrations.CreateModel(name='RecoverableLoadRatio', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'code', models.CharField(max_length=50, verbose_name='account')),
      (
       'ratio', models.DecimalField(decimal_places=0, default=100, max_digits=4, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='ratio'))], options={'verbose_name': 'recoverable load ratio', 
      'verbose_name_plural': 'recoverable load ratios', 
      'ordering': ['code'], 
      'default_permissions': []}),
     migrations.RunPython(printer_model)]