# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/accounts/migrations/0003_auto_20190607_1540.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 925 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('accounts', '0002_auto_20180103_1628')]
    operations = [
     migrations.AddField(model_name='account',
       name='email_index',
       field=models.CharField(default=False, max_length=255)),
     migrations.AddField(model_name='account',
       name='encrypted_email',
       field=models.CharField(default=False, max_length=255)),
     migrations.AddField(model_name='account',
       name='encrypted_username',
       field=models.CharField(default=False, max_length=255)),
     migrations.AddField(model_name='account',
       name='username_index',
       field=models.CharField(default=False, max_length=255))]