# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/buttons/migrations/0004_auto_20181125_2227.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1261 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('buttons', '0003_button_icon_color')]
    operations = [
     migrations.AlterModelOptions(name='button',
       options={'verbose_name':'\\u0628\\u0627\\u062a\\u0646', 
      'verbose_name_plural':'\\u0628\\u0627\\u062a\\u0646 \\u0647\\u0627'}),
     migrations.AlterModelOptions(name='buttonsegment',
       options={'verbose_name':'\\u0628\\u062e\\u0634 \\u0628\\u0627\\u062a\\u0646', 
      'verbose_name_plural':'\\u0628\\u062e\\u0634 \\u0628\\u0627\\u062a\\u0646 \\u0647\\u0627'}),
     migrations.AlterField(model_name='button',
       name='background_color',
       field=models.CharField(blank=True, max_length=6, null=True, verbose_name='\\u0631\\u0646\\u06af \\u067e\\u0633 \\u0632\\u0645\\u06cc\\u0646\\u0647')),
     migrations.AlterField(model_name='button',
       name='icon_color',
       field=models.CharField(blank=True, max_length=6, null=True, verbose_name='\\u0631\\u0646\\u06af \\u0622\\u06cc\\u06a9\\u0646'))]