# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/0P/01-dajngo/3d/app/usuarios/migrations/0002_user_is_staff.py
# Compiled at: 2018-03-15 13:40:11
# Size of source mod 2**32: 475 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('usuarios', '0001_initial')]
    operations = [
     migrations.AddField(model_name='user',
       name='is_staff',
       field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'))]