# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0008_userprofile_accounting_number_data.py
# Compiled at: 2017-01-14 18:46:55
# Size of source mod 2**32: 862 bytes
from __future__ import unicode_literals
import billjobs.validators
from django.db import migrations, models

def create_accounting_number(apps, schema_editor):
    """ Data migration to create accounting number in existing profiles"""
    UserProfile = apps.get_model('billjobs', 'UserProfile')
    for profile in UserProfile.objects.all():
        profile.accounting_number = set_user_profile_accounting_number(profile.user.last_name, profile.user.first_name)
        profile.save()


class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0007_userprofile_accounting_number')]
    operations = [
     migrations.RunPython(create_accounting_number)]