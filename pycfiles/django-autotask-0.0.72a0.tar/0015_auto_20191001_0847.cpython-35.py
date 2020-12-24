# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0015_auto_20191001_0847.py
# Compiled at: 2019-10-08 19:20:37
# Size of source mod 2**32: 1583 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0014_auto_20190930_1548')]
    operations = [
     migrations.CreateModel(name='DisplayColor', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'label', models.CharField(blank=True, max_length=50, null=True)),
      (
       'is_default_value', models.BooleanField(default=False)),
      (
       'sort_order', models.PositiveSmallIntegerField(blank=True, null=True)),
      (
       'parent_value', models.CharField(blank=True, max_length=20, null=True)),
      (
       'is_active', models.BooleanField(default=False)),
      (
       'is_system', models.BooleanField(default=False))], options={'verbose_name_plural': 'Display colors'}),
     migrations.AddField(model_name='ticketcategory', name='display_color', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.DisplayColor'))]