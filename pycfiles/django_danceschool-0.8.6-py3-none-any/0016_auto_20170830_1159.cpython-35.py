# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0016_auto_20170830_1159.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 1803 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0015_auto_20170829_1301')]
    operations = [
     migrations.RenameField(model_name='pricingtier', old_name='doorGeneralPrice', new_name='doorPrice'),
     migrations.RenameField(model_name='pricingtier', old_name='onlineGeneralPrice', new_name='onlinePrice'),
     migrations.RemoveField(model_name='pricingtier', name='doorStudentPrice'),
     migrations.RemoveField(model_name='pricingtier', name='onlineStudentPrice'),
     migrations.AlterField(model_name='invoice', name='temporaryRegistration', field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.TemporaryRegistration', verbose_name='Temporary registration')),
     migrations.AlterField(model_name='invoiceitem', name='temporaryEventRegistration', field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.TemporaryEventRegistration', verbose_name='Temporary event registration')),
     migrations.AlterField(model_name='registration', name='temporaryRegistration', field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.TemporaryRegistration', verbose_name='Associated temporary registration'))]