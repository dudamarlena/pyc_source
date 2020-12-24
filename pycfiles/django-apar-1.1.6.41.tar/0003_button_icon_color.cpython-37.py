# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0003_button_icon_color.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 468 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0002_button_background_color')]
    operations = [
     migrations.AddField(model_name='button',
       name='icon_color',
       field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Icon color'))]