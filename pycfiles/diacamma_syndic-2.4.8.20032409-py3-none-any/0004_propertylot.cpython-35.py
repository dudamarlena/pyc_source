# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/migrations/0004_propertylot.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 1492 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('condominium', '0003_callfunds_expense_status')]
    operations = [
     migrations.CreateModel(name='PropertyLot', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'num', models.IntegerField(default=1, verbose_name='numeros')),
      (
       'value', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='tantime')),
      (
       'description', models.TextField(default='', null=True, verbose_name='description')),
      (
       'owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominium.Owner', verbose_name='owner'))], options={'verbose_name': 'property lot', 
      'ordering': ['num'], 
      'verbose_name_plural': 'property lots', 
      'default_permissions': []}),
     migrations.AlterModelOptions(name='set', options={'verbose_name': 'class load', 'verbose_name_plural': 'class loads'})]