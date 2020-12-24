# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/frank/.virtualenvs/venv2/generator/test_app/migrations/0001_initial.py
# Compiled at: 2018-04-07 16:46:46
# Size of source mod 2**32: 791 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='Product',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'order_id', models.CharField(editable=False, max_length=11, null=True, unique=True, verbose_name='Article Refrence')),
      (
       'article_name', models.CharField(max_length=128, verbose_name='Article name'))],
       options={'verbose_name':'Product', 
      'verbose_name_plural':'Products'})]