# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michal/workspace/code/django-mips/mips/migrations/0001_initial.py
# Compiled at: 2015-11-17 09:55:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = []
    operations = [
     migrations.CreateModel(name=b'Instance', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mip_pool', models.IntegerField()),
      (
       b'mip_production_data', models.DateField()),
      (
       b'mip_producer', models.CharField(max_length=255)),
      (
       b'mip_plate', models.CharField(max_length=255)),
      (
       b'mip_position', models.CharField(max_length=50)),
      (
       b'mip_instance', models.IntegerField())]),
     migrations.CreateModel(name=b'Mip', fields=[
      (
       b'mip_id', models.IntegerField(unique=True, serialize=False, primary_key=True)),
      (
       b'mip_sequence', models.TextField()),
      (
       b'mip_extension_arm', models.TextField()),
      (
       b'mip_ligation_arm', models.TextField()),
      (
       b'mip_func_immuno', models.BooleanField(default=False)),
      (
       b'mip_func_mapping', models.BooleanField(default=False)),
      (
       b'mip_func_random', models.BooleanField(default=False)),
      (
       b'mip_func_utr', models.BooleanField(default=False)),
      (
       b'mip_start', models.IntegerField()),
      (
       b'mip_stop', models.IntegerField()),
      (
       b'reference_id', models.TextField(null=True)),
      (
       b'mip_comments', models.TextField(null=True))]),
     migrations.CreateModel(name=b'Paralog', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mip_subspecies_paralog', models.CharField(max_length=50)),
      (
       b'mip_fk', models.ForeignKey(to=b'mips.Mip'))]),
     migrations.CreateModel(name=b'Samples', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'mip_sequence', models.TextField()),
      (
       b'mip_performance', models.BooleanField(default=False)),
      (
       b'mip_fk', models.ForeignKey(to=b'mips.Mip'))]),
     migrations.CreateModel(name=b'SampleSubspecies', fields=[
      (
       b'sample_id', models.IntegerField(serialize=False, primary_key=True))]),
     migrations.CreateModel(name=b'Subspecies', fields=[
      (
       b'subspecies', models.CharField(max_length=255, serialize=False, primary_key=True))]),
     migrations.AddField(model_name=b'samplesubspecies', name=b'subspecies_fk', field=models.ForeignKey(to=b'mips.Subspecies')),
     migrations.AddField(model_name=b'samples', name=b'sample_fk', field=models.ForeignKey(to=b'mips.SampleSubspecies')),
     migrations.AddField(model_name=b'paralog', name=b'subspecies_fk', field=models.ForeignKey(to=b'mips.Subspecies')),
     migrations.AddField(model_name=b'instance', name=b'mip_fk', field=models.ForeignKey(to=b'mips.Mip'))]