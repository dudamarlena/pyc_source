# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/migrations/0005_baseuser_language.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 422 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0004_usergroup_authenticate_with_phone_otp')]
    operations = [
     migrations.AddField(model_name='baseuser',
       name='language',
       field=models.CharField(default='EN', max_length=255))]