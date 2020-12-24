# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0006_additional_validator_many_to_many.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0005_added_enum_generic_relation')]
    operations = [
     migrations.CreateModel(name=b'Validator', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'validator', models.CharField(max_length=128))]),
     migrations.RemoveField(model_name=b'formfield', name=b'additional_validators'),
     migrations.AddField(model_name=b'formfield', name=b'additional_validators', field=models.ManyToManyField(to=b'formfactory.Validator'))]