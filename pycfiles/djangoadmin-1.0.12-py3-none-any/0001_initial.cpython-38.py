# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangoadmin\src\djangoadmin\migrations\0001_initial.py
# Compiled at: 2019-05-13 06:06:01
# Size of source mod 2**32: 1199 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='UserModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'image', models.ImageField(blank=True, null=True, upload_to='djangoadmin')),
      (
       'address', models.CharField(blank=True, max_length=100, null=True)),
      (
       'phone', models.BigIntegerField(blank=True, null=True)),
      (
       'website', models.URLField(blank=True, null=True)),
      (
       'user', models.OneToOneField(on_delete=(django.db.models.deletion.CASCADE), to=(settings.AUTH_USER_MODEL)))],
       options={'verbose_name':'User', 
      'verbose_name_plural':'Users', 
      'ordering':[
       'pk']})]