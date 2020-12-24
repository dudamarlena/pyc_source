# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0005_auto_20190501_1142.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 1517 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0004_filefield_title')]
    operations = [
     migrations.AddField(model_name='filefield',
       name='is_encrypt_needed',
       field=models.BooleanField(default=False, verbose_name='Is encrypt needed?')),
     migrations.AddField(model_name='filefield',
       name='is_lock',
       field=models.BooleanField(default=False, verbose_name='Is lock?')),
     migrations.AddField(model_name='filefield',
       name='iv',
       field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='IV')),
     migrations.AddField(model_name='filefield',
       name='password',
       field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='\\u06af\\u0630\\u0631\\u0648\\u0627\\u0698\\u0647')),
     migrations.AlterField(model_name='filefield',
       name='type',
       field=models.CharField(blank=True, choices=[('M', '\\u0641\\u06cc\\u0644\\u0645'), ('V', '\\u0635\\u062f\\u0627'), ('P', '\\u067e\\u06cc \\u062f\\u06cc \\u0627\\u0641'), ('I', '\\u0639\\u06a9\\u0633')], max_length=1, null=True, verbose_name='\\u0646\\u0648\\u0639 \\u0641\\u0627\\u06cc\\u0644'))]