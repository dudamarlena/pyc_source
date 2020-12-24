# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0005_button_title_color.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 465 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0004_auto_20181125_2227')]
    operations = [
     migrations.AddField(model_name='button',
       name='title_color',
       field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Title color'))]