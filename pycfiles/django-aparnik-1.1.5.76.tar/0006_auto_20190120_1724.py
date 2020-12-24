# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0006_auto_20190120_1724.py
# Compiled at: 2019-01-31 06:07:32
from __future__ import unicode_literals
import colorfield.fields
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0005_button_title_color')]
    operations = [
     migrations.AlterField(model_name=b'button', name=b'background_color', field=colorfield.fields.ColorField(default=b'#2672DF', max_length=18, verbose_name=b'رنگ پس زمینه')),
     migrations.AlterField(model_name=b'button', name=b'icon_color', field=colorfield.fields.ColorField(default=b'#2672DF', max_length=18, verbose_name=b'رنگ آیکن')),
     migrations.AlterField(model_name=b'button', name=b'title_color', field=colorfield.fields.ColorField(default=b'#2672DF', max_length=18, verbose_name=b'Title color'))]