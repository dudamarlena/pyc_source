# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adminlteui/migrations/0001_initial.py
# Compiled at: 2020-05-05 22:21:28
# Size of source mod 2**32: 985 bytes
from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Options',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'option_name', models.CharField(max_length=255, unique=True, verbose_name='Option Name')),
      (
       'option_value', models.TextField(verbose_name='Option Value')),
      (
       'create_time', models.DateTimeField(default=(timezone.now), verbose_name='CreateTime')),
      (
       'update_time', models.DateTimeField(auto_now=True, verbose_name='UpdateTime'))],
       options={'verbose_name':'Options', 
      'verbose_name_plural':'All Options'})]