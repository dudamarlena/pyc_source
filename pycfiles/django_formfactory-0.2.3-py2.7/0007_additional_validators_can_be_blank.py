# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0007_additional_validators_can_be_blank.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0006_additional_validator_many_to_many')]
    operations = [
     migrations.AlterField(model_name=b'formfield', name=b'additional_validators', field=models.ManyToManyField(blank=True, to=b'formfactory.Validator'))]