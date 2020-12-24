# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/admin/migrations/0007_auto_20161124_1811.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 704 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('admin', '0006_organization_organizationrole')]
    operations = [
     migrations.AlterField(model_name='user',
       name='is_superuser',
       field=djangoplus.db.models.fields.BooleanField(default=True, verbose_name='Superusuário?')),
     migrations.AlterField(model_name='user',
       name='password',
       field=djangoplus.db.models.fields.CharField(max_length=128, verbose_name='Senha'))]