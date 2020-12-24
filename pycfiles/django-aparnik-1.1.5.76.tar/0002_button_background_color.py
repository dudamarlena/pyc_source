# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0002_button_background_color.py
# Compiled at: 2018-11-25 11:27:48
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'button', name=b'background_color', field=models.CharField(blank=True, max_length=6, null=True, verbose_name=b'Background Color'))]