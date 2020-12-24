# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dwjor/Google Drive/Code/Python/django-cryptapi/cryptapi/migrations/0003_auto_20181112_1939.py
# Compiled at: 2020-05-04 20:02:30
# Size of source mod 2**32: 442 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('cryptapi', '0002_provider_last_updated')]
    operations = [
     migrations.AlterField(model_name='request',
       name='nonce',
       field=models.CharField(default='', max_length=32, verbose_name='Nonce'))]