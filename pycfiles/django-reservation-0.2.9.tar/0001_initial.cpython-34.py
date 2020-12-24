# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/organilab/djreservation/migrations/0001_initial.py
# Compiled at: 2016-09-02 22:40:04
# Size of source mod 2**32: 2038 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('contenttypes', '0002_remove_content_type_name')]
    operations = [
     migrations.CreateModel(name='Product', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'amount', models.FloatField()),
      (
       'amount_field', models.CharField(max_length=150)),
      (
       'borrowed', models.BooleanField(default=False)),
      (
       'object_id', models.PositiveIntegerField()),
      (
       'content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'))]),
     migrations.CreateModel(name='Reservation', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'reserved_start_date', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'return_date', models.DateTimeField()),
      (
       'status', models.SmallIntegerField(choices=[(0, 'building'), (1, 'Requested'), (2, 'Acepted'), (3, 'Denied'), (4, 'Returned')], default=0)),
      (
       'updated_datetime', models.DateTimeField(auto_now=True)),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.AddField(model_name='product', name='reservation', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djreservation.Reservation'))]