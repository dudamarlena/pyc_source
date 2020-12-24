# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0010_auto_20170428_1545.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 813 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('auth', '0008_alter_user_username_max_length'),
     ('admin', '0009_auto_20170420_1238')]
    operations = [
     migrations.CreateModel(name='Permission',
       fields=[],
       options={'verbose_name':'Permissão', 
      'proxy':True, 
      'verbose_name_plural':'Permissões', 
      'indexes':[]},
       bases=('auth.permission', )),
     migrations.AlterModelOptions(name='group',
       options={'verbose_name':'Grupo', 
      'verbose_name_plural':'Grupos'})]