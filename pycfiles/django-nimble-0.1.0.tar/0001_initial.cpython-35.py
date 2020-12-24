# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\migrations\0001_initial.py
# Compiled at: 2016-11-19 14:34:52
# Size of source mod 2**32: 1263 bytes
from __future__ import unicode_literals
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def create_profiles_for_existing_users(apps, scheme_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('nimble', 'Profile')
    for instance in User.objects.all():
        if hasattr(instance, 'profile'):
            pass
        else:
            profile = Profile.objects.create(user=instance)
            profile.save


class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
     migrations.CreateModel(name='Profile', fields=[
      (
       'id',
       models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'user',
       models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
     migrations.RunPython(create_profiles_for_existing_users)]