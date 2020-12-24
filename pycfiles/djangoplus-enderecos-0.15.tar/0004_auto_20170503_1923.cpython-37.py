# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/enderecos/migrations/0004_auto_20170503_1923.py
# Compiled at: 2018-10-05 12:52:35
# Size of source mod 2**32: 390 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('enderecos', '0003_delete_telefone')]
    operations = [
     migrations.RenameField(model_name='bairro',
       old_name='cidade',
       new_name='municipio')]