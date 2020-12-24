# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0038_notetype_tasknote_ticketnote.py
# Compiled at: 2020-01-31 18:17:22
# Size of source mod 2**32: 4027 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0037_subissuetype_parent_value')]
    operations = [
     migrations.CreateModel(name='NoteType', fields=[
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
       'is_active', models.BooleanField(default=False)),
      (
       'is_system', models.BooleanField(default=False))], options={'abstract': False, 
      'ordering': ('label', )}),
     migrations.CreateModel(name='TaskNote', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'title', models.CharField(max_length=250)),
      (
       'description', models.CharField(max_length=3200)),
      (
       'create_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'last_activity_date', models.DateTimeField(blank=True, null=True)),
      (
       'creator_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Resource')),
      (
       'note_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.NoteType')),
      (
       'task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Task'))], options={'abstract': False, 
      'ordering': ('-modified', '-created'), 
      'get_latest_by': 'modified'}),
     migrations.CreateModel(name='TicketNote', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'title', models.CharField(max_length=250)),
      (
       'description', models.CharField(max_length=3200)),
      (
       'create_date_time', models.DateTimeField(blank=True, null=True)),
      (
       'last_activity_date', models.DateTimeField(blank=True, null=True)),
      (
       'creator_resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Resource')),
      (
       'note_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.NoteType')),
      (
       'ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.Ticket'))], options={'abstract': False, 
      'ordering': ('-modified', '-created'), 
      'get_latest_by': 'modified'})]