# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/transmanager/transmanager/migrations/0003_auto_20160513_2151.py
# Compiled at: 2016-06-01 06:08:22
# Size of source mod 2**32: 1101 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('transmanager', '0002_transitemlanguage')]
    operations = [
     migrations.AlterModelOptions(name='transitemlanguage', options={'verbose_name': 'Idiomas por item',  'verbose_name_plural': 'Idiomas por item'}),
     migrations.AlterField(model_name='transitemlanguage', name='content_type', field=models.ForeignKey(to='contenttypes.ContentType', verbose_name='Modelo')),
     migrations.AlterField(model_name='transitemlanguage', name='languages', field=models.ManyToManyField(verbose_name='Idiomas', to='transmanager.TransLanguage', help_text='Idiomas por defecto del item')),
     migrations.AlterField(model_name='transitemlanguage', name='object_id', field=models.PositiveIntegerField(verbose_name='Identificador'))]