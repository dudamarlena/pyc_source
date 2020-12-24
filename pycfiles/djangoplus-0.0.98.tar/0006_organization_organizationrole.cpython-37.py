# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/migrations/0006_organization_organizationrole.py
# Compiled at: 2018-10-05 12:53:01
# Size of source mod 2**32: 1558 bytes
from django.db import migrations, models
import django.db.models.deletion, djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0005_auto_20161005_1536')]
    operations = [
     migrations.CreateModel(name='Organization',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'ascii', djangoplus.db.models.fields.SearchField(blank=True, default=b'', editable=False))],
       options={'verbose_name':'Organização', 
      'verbose_name_plural':'Organizações'}),
     migrations.CreateModel(name='OrganizationRole',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'organization', djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to='admin.Organization', verbose_name='Organização')),
      (
       'role', djangoplus.db.models.fields.ModelChoiceField(on_delete=(django.db.models.deletion.CASCADE), to='admin.Role', verbose_name='Função'))],
       options={'verbose_name':'Papel na Organização', 
      'verbose_name_plural':'Papeis na Organização'})]