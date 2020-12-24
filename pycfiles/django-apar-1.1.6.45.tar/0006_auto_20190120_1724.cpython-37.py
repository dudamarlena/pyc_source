# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0006_auto_20190120_1724.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1031 bytes
import colorfield.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0005_button_title_color')]
    operations = [
     migrations.AlterField(model_name='button',
       name='background_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='\\u0631\\u0646\\u06af \\u067e\\u0633 \\u0632\\u0645\\u06cc\\u0646\\u0647')),
     migrations.AlterField(model_name='button',
       name='icon_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='\\u0631\\u0646\\u06af \\u0622\\u06cc\\u06a9\\u0646')),
     migrations.AlterField(model_name='button',
       name='title_color',
       field=colorfield.fields.ColorField(default='#2672DF', max_length=18, verbose_name='Title color'))]