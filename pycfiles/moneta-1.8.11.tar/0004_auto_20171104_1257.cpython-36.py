# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/migrations/0004_auto_20171104_1257.py
# Compiled at: 2017-11-04 07:57:50
# Size of source mod 2**32: 1158 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('repository', '0003_auto_20170306_2202')]
    operations = [
     migrations.AlterField(model_name='archivestate',
       name='author',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), verbose_name='Auteur')),
     migrations.AlterField(model_name='element',
       name='author',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), verbose_name='Auteur')),
     migrations.AlterField(model_name='repository',
       name='author',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.SET_NULL), to=(settings.AUTH_USER_MODEL), verbose_name='Auteur'))]