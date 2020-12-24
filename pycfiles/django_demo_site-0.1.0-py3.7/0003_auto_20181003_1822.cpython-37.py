# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\demo_site\migrations\0003_auto_20181003_1822.py
# Compiled at: 2018-10-03 12:22:41
# Size of source mod 2**32: 605 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('demo_site', '0002_auto_20181003_1634')]
    operations = [
     migrations.AlterField(model_name='demositesettings',
       name='text',
       field=models.TextField(default='This is a website under active development and may have bugs and lack lots of features. If you find anything you want to report use the contact email or issue handler below.', verbose_name='Text'))]