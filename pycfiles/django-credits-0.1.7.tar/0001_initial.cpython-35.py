# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rerb/.virtualenvs/django-credits-demo/lib/python3.5/site-packages/django_credits-0.1.2-py3.5.egg/django_credits/migrations/0001_initial.py
# Compiled at: 2016-07-14 00:12:15
# Size of source mod 2**32: 2078 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Contribution', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'))]),
     migrations.CreateModel(name='Contributor', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'given_name', models.CharField(blank=True, max_length=255, null=True)),
      (
       'family_name', models.CharField(blank=True, db_index=True, max_length=255, null=True))], options={'ordering': ('family_name', 'given_name')}),
     migrations.CreateModel(name='Credit', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'headline', models.CharField(max_length=255)),
      (
       'ordinal', models.PositiveIntegerField(blank=True, db_index=True)),
      (
       'contributors', models.ManyToManyField(blank=True, through='django_credits.Contribution', to='django_credits.Contributor'))], options={'ordering': ('ordinal', )}),
     migrations.AddField(model_name='contribution', name='contributor', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_credits.Contributor')),
     migrations.AddField(model_name='contribution', name='credit', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_credits.Credit'))]