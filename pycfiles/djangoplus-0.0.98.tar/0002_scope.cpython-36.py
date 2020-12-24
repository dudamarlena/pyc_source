# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0002_scope.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 733 bytes
from django.db import migrations, models
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0001_squashed_0015_settings_company')]
    operations = [
     migrations.CreateModel(name='Scope',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'ascii', djangoplus.db.models.fields.SearchField(blank=True, default='', editable=False))],
       options={'verbose_name':'Scope', 
      'verbose_name_plural':'Scopes'})]