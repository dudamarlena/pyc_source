# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/migrations/0015_auto_20170829_1301.py
# Compiled at: 2019-04-03 22:56:26
# Size of source mod 2**32: 1447 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0014_auto_20170821_1226')]
    operations = [
     migrations.AddField(model_name='temporaryregistration',
       name='expirationDate',
       field=models.DateTimeField(default=(django.utils.timezone.now), help_text='When a customer attempts to begin the registration process, the system looks for temporary registrations that are still in progress (with a future expiration date) to determine if there is space for them to register.', verbose_name='Expiration date'),
       preserve_default=False),
     migrations.AlterField(model_name='temporaryregistration',
       name='email',
       field=models.CharField(max_length=200, null=True, verbose_name='Email address')),
     migrations.AlterField(model_name='temporaryregistration',
       name='firstName',
       field=models.CharField(max_length=100, null=True, verbose_name='First name')),
     migrations.AlterField(model_name='temporaryregistration',
       name='lastName',
       field=models.CharField(max_length=100, null=True, verbose_name='Last name'))]