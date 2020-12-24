# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/migrations/0009_auto_20190114_2126.py
# Compiled at: 2019-02-28 16:17:24
# Size of source mod 2**32: 1167 bytes
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('billjobs', '0008_auto_20180308_1312')]
    operations = [
     migrations.AlterField(model_name='bill',
       name='user',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to=(settings.AUTH_USER_MODEL), verbose_name='Coworker')),
     migrations.AlterField(model_name='billline',
       name='bill',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to='billjobs.Bill')),
     migrations.AlterField(model_name='billline',
       name='service',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.PROTECT), to='billjobs.Service')),
     migrations.AlterField(model_name='userprofile',
       name='user',
       field=models.OneToOneField(on_delete=(django.db.models.deletion.PROTECT), to=(settings.AUTH_USER_MODEL)))]