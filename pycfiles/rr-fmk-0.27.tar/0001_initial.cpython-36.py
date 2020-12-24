# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/0P/01-dajngo/3d/app/usuarios/migrations/0001_initial.py
# Compiled at: 2018-03-15 14:09:30
# Size of source mod 2**32: 746 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Cliente',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'department', models.CharField(max_length=100)),
      (
       'user', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))])]