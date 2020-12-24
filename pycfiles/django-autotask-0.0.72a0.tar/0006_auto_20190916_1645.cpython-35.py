# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sam/git/Kanban/django-autotask/djautotask/migrations/0006_auto_20190916_1645.py
# Compiled at: 2019-10-01 19:08:49
# Size of source mod 2**32: 1723 bytes
from django.db import migrations, models
import django.db.models.deletion, django_extensions.db.fields

class Migration(migrations.Migration):
    dependencies = [
     ('djautotask', '0005_auto_20190916_1549')]
    operations = [
     migrations.CreateModel(name='TicketPriority', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
      (
       'value', models.CharField(blank=True, max_length=50, null=True)),
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
       'is_system', models.BooleanField(default=False))], options={'verbose_name': 'Ticket priority', 
      'verbose_name_plural': 'Ticket priorities'}),
     migrations.AddField(model_name='ticket', name='priority', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djautotask.TicketPriority'))]