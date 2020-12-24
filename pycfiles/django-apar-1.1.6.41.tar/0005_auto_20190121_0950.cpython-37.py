# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/managements/migrations/0005_auto_20190121_0950.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 541 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('managements', '0004_fieldlist_group')]
    operations = [
     migrations.AlterField(model_name='fieldlist',
       name='group',
       field=models.ForeignKey(blank=True, null=True, on_delete=(django.db.models.deletion.CASCADE), to='auth.Group', verbose_name='group'))]