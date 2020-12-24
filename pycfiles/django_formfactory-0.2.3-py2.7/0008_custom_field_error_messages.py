# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0008_custom_field_error_messages.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0007_additional_validators_can_be_blank')]
    operations = [
     migrations.CreateModel(name=b'CustomErrorMessage', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'key', models.CharField(choices=[], max_length=128)),
      (
       b'value', models.CharField(max_length=256))]),
     migrations.AddField(model_name=b'formfield', name=b'error_messages', field=models.ManyToManyField(blank=True, to=b'formfactory.CustomErrorMessage'))]