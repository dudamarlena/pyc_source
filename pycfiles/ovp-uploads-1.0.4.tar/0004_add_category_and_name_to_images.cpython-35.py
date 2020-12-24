# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/migrations/0004_add_category_and_name_to_images.py
# Compiled at: 2017-06-13 10:26:46
# Size of source mod 2**32: 1015 bytes
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('ovp_uploads', '0003_uploadedimage_uuid')]
    operations = [
     migrations.CreateModel(name='ImageGalery', fields=[], options={'proxy': True}, bases=('ovp_uploads.uploadedimage', )),
     migrations.AddField(model_name='uploadedimage', name='category', field=models.CharField(blank=True, choices=[('cover', 'Cover'), ('logo', 'Logo')], default=None, max_length=24, null=True, verbose_name='Category')),
     migrations.AddField(model_name='uploadedimage', name='name', field=models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='Name'))]