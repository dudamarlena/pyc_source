# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\AppData\Local\Temp\pip-install-9f4wujyx\steemconnect-auth\steemconnect_auth\migrations\0003_auto_20190205_1935.py
# Compiled at: 2019-05-20 22:11:00
# Size of source mod 2**32: 375 bytes
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
     ('steemconnect_auth', '0002_auto_20190205_1932')]
    operations = [
     migrations.AlterModelTable(name='steemconnectuser',
       table='SteemConnectUser')]