# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/migrations/0001_initial.py
# Compiled at: 2020-04-03 10:42:48
# Size of source mod 2**32: 2028 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, phonenumber_field.modelfields

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='PhoneNumber',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
      (
       'verified', models.BooleanField(default=False, verbose_name='verified')),
      (
       'primary', models.BooleanField(default=False, verbose_name='primary')),
      (
       'user', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='user_phone', to=(settings.AUTH_USER_MODEL)))],
       options={'verbose_name':'phone number ', 
      'verbose_name_plural':'Phone Numbers'}),
     migrations.CreateModel(name='PhoneNumberConfirmation',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'pin', models.IntegerField(max_length=6, unique=True, verbose_name='pin')),
      (
       'sent', models.DateTimeField(null=True, verbose_name='sent')),
      (
       'phone_number', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), related_name='phone_number', to='phonenumber_confirmation.PhoneNumber'))],
       options={'verbose_name':'phone number confirmation', 
      'verbose_name_plural':'Phone Number Confirmations'})]