# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/pessoas/migrations/0002_pessoa_tipo.py
# Compiled at: 2018-10-05 12:53:22
# Size of source mod 2**32: 593 bytes
from django.db import migrations
import djangoplus.db.models.fields

class Migration(migrations.Migration):
    dependencies = [
     ('pessoas', '0001_initial')]
    operations = [
     migrations.AddField(model_name='pessoa',
       name='tipo',
       field=djangoplus.db.models.fields.CharField(choices=[['Física', 'Física'], ['Jurídica', 'Jurídica']], default='Física', max_length=255, verbose_name='Tipo'),
       preserve_default=False)]