# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/snappion_backend/avishan/migrations/0004_usergroup_authenticate_with_phone_otp.py
# Compiled at: 2020-02-15 16:12:24
# Size of source mod 2**32: 413 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('avishan', '0003_requesttrackexecinfo')]
    operations = [
     migrations.AddField(model_name='usergroup',
       name='authenticate_with_phone_otp',
       field=models.BooleanField(default=False))]