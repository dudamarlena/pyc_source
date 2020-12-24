# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0014_auto_20190930_1548.py
# Compiled at: 2019-10-08 19:20:37
# Size of source mod 2**32: 6182 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0013_auto_20190923_1439')]
    operations = [
     migrations.CreateModel(name='IssueType', fields=[
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
       'is_system', models.BooleanField(default=False))], options={'abstract': False}),
     migrations.CreateModel(name='Source', fields=[
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
       'is_system', models.BooleanField(default=False))], options={'abstract': False}),
     migrations.CreateModel(name='SubIssueType', fields=[
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
       'is_system', models.BooleanField(default=False))], options={'abstract': False}),
     migrations.CreateModel(name='TicketCategory', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'name', models.CharField(max_length=30)),
      (
       'active', models.BooleanField(default=False))], options={'verbose_name_plural': 'Ticket categories'}),
     migrations.CreateModel(name='TicketType', fields=[
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
       'is_system', models.BooleanField(default=False))], options={'abstract': False}),
     migrations.AddField(model_name='ticket', name='category', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.TicketCategory')),
     migrations.AddField(model_name='ticket', name='issue_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.IssueType')),
     migrations.AddField(model_name='ticket', name='source', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Source')),
     migrations.AddField(model_name='ticket', name='sub_issue_type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.SubIssueType')),
     migrations.AddField(model_name='ticket', name='type', field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.TicketType'))]