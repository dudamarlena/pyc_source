# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/ohm2-dev-light/backend/webapp/backend/apps/ohm2_accounts_light/migrations/0001_squashed_0003_auto_20181119_2119.py
# Compiled at: 2018-11-19 16:20:07
# Size of source mod 2**32: 1562 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django.utils.timezone

class Migration(migrations.Migration):
    replaces = [
     ('ohm2_accounts_light', '0001_initial'), ('ohm2_accounts_light', '0002_auto_20181119_2052'), ('ohm2_accounts_light', '0003_auto_20181119_2119')]
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='PasswordReset', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'identity', models.CharField(max_length=255, unique=True)),
      (
       'created', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_update', models.DateTimeField(default=django.utils.timezone.now)),
      (
       'last_sent_date', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'activation_date', models.DateTimeField(blank=True, default=None, null=True)),
      (
       'ip_address', models.GenericIPAddressField(blank=True, default='', null=True)),
      (
       'code', models.CharField(max_length=255, unique=True)),
      (
       'user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'abstract': False})]