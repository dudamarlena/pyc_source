# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0004_auto_20181125_2227.py
# Compiled at: 2018-11-26 02:58:29
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0003_button_icon_color')]
    operations = [
     migrations.AlterModelOptions(name=b'button', options={b'verbose_name': b'باتن', b'verbose_name_plural': b'باتن ها'}),
     migrations.AlterModelOptions(name=b'buttonsegment', options={b'verbose_name': b'بخش باتن', b'verbose_name_plural': b'بخش باتن ها'}),
     migrations.AlterField(model_name=b'button', name=b'background_color', field=models.CharField(blank=True, max_length=6, null=True, verbose_name=b'رنگ پس زمینه')),
     migrations.AlterField(model_name=b'button', name=b'icon_color', field=models.CharField(blank=True, max_length=6, null=True, verbose_name=b'رنگ آیکن'))]