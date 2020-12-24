# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0007_userprofile_accounting_number.py
# Compiled at: 2017-01-14 18:47:36
# Size of source mod 2**32: 1296 bytes
from __future__ import unicode_literals
import billjobs.validators
from django.db import migrations, models
from billjobs.models import set_user_profile_accounting_number

def create_accounting_number(apps, schema_editor):
    """ Data migration to create accounting number in existing profiles"""
    UserProfile = apps.get_model('billjobs', 'UserProfile')
    for profile in UserProfile.objects.all():
        profile.accounting_number = set_user_profile_accounting_number(profile.user.last_name, profile.user.first_name)
        profile.save()


class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0006_add_billin_address_and_migrate_data')]
    operations = [
     migrations.AddField(model_name='userprofile',
       name='accounting_number',
       field=models.CharField(max_length=8,
       null=True,
       blank=True,
       validators=[
      billjobs.validators.validate_accounting_number],
       verbose_name='Accounting number')),
     migrations.RunPython(create_accounting_number)]