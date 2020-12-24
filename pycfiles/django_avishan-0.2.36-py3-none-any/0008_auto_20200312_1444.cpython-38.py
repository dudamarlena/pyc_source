# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/migrations/0008_auto_20200312_1444.py
# Compiled at: 2020-04-21 05:34:55
# Size of source mod 2**32: 608 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0007_visitorkey')]
    operations = [
     migrations.RemoveField(model_name='usergroup',
       name='authenticate_with_email_password'),
     migrations.RemoveField(model_name='usergroup',
       name='authenticate_with_phone_otp'),
     migrations.RemoveField(model_name='usergroup',
       name='authenticate_with_phone_password')]