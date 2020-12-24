# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/migrations/0002_translatablechar.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 715 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0001_initial')]
    operations = [
     migrations.CreateModel(name='TranslatableChar',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'en', models.CharField(blank=True, default=None, max_length=255, null=True)),
      (
       'fa', models.CharField(blank=True, default=None, max_length=255, null=True))],
       options={'abstract': False})]