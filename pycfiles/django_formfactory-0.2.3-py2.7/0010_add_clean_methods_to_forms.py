# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/migrations/0010_add_clean_methods_to_forms.py
# Compiled at: 2017-09-07 07:30:48
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('formfactory', '0009_form_enable_csrf')]
    operations = [
     migrations.CreateModel(name=b'CleanMethod', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'clean_method', models.CharField(max_length=128))]),
     migrations.AlterModelOptions(name=b'customerrormessage', options={b'verbose_name': b'Field error message', b'verbose_name_plural': b'Field error messages'}),
     migrations.AddField(model_name=b'form', name=b'clean_method', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=b'formfactory.CleanMethod'))]