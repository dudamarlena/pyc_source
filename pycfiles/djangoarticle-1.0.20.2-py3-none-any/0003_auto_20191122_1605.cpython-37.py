# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoarticle\src\djangoarticle\migrations\0003_auto_20191122_1605.py
# Compiled at: 2019-11-22 05:35:53
# Size of source mod 2**32: 1657 bytes
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('djangoarticle', '0002_auto_20190724_1927')]
    operations = [
     migrations.AddField(model_name='articlemodelscheme',
       name='created_at',
       field=models.DateTimeField(auto_now_add=True, default=(django.utils.timezone.now)),
       preserve_default=False),
     migrations.AddField(model_name='articlemodelscheme',
       name='updated_at',
       field=models.DateTimeField(auto_now=True)),
     migrations.AlterField(model_name='articlemodelscheme',
       name='shortlines',
       field=models.TextField(blank=True, null=True)),
     migrations.AlterField(model_name='articlemodelscheme',
       name='status',
       field=models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish'), ('withdraw', 'Withdraw'), ('private', 'Private')], default='draft', max_length=20)),
     migrations.AlterField(model_name='articlemodelscheme',
       name='title',
       field=models.CharField(max_length=95, unique=True)),
     migrations.AlterField(model_name='categorymodelscheme',
       name='status',
       field=models.CharField(choices=[('draft', 'Draft'), ('publish', 'Publish'), ('withdraw', 'Withdraw'), ('private', 'Private')], default='draft', max_length=20))]