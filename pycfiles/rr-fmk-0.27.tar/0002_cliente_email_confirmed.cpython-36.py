# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/usuarios/migrations/0002_cliente_email_confirmed.py
# Compiled at: 2018-03-28 11:46:11
# Size of source mod 2**32: 387 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('usuarios', '0001_initial')]
    operations = [
     migrations.AddField(model_name='cliente',
       name='email_confirmed',
       field=models.BooleanField(default=False))]