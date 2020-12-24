# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\AppData\Local\Temp\pip-install-9f4wujyx\steemconnect-auth\steemconnect_auth\migrations\0005_auto_20190205_2046.py
# Compiled at: 2019-05-20 22:11:00
# Size of source mod 2**32: 1299 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('steemconnect_auth', '0004_auto_20190205_1941')]
    operations = [
     migrations.AlterModelOptions(name='steemconnectuser',
       options={}),
     migrations.AlterModelManagers(name='steemconnectuser',
       managers=[]),
     migrations.RemoveField(model_name='steemconnectuser',
       name='user_ptr'),
     migrations.AddField(model_name='steemconnectuser',
       name='id',
       field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
       preserve_default=False),
     migrations.AddField(model_name='steemconnectuser',
       name='user',
       field=models.OneToOneField(default=1, on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)),
       preserve_default=False)]