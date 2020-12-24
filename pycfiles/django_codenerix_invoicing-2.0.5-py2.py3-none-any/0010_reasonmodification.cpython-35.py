# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0010_reasonmodification.py
# Compiled at: 2018-02-02 06:33:24
# Size of source mod 2**32: 1143 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0009_salesorderdocument')]
    operations = [
     migrations.CreateModel(name='ReasonModification', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'code', models.CharField(max_length=15, unique=True, verbose_name='Code')),
      (
       'name', models.CharField(max_length=250, verbose_name='Name')),
      (
       'enable', models.BooleanField(default=True, verbose_name='Enable'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')})]