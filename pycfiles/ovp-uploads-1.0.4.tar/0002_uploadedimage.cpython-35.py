# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/migrations/0002_uploadedimage.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1774 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion, django_resized.forms, ovp_uploads.models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     migrations.swappable_dependency(settings.AUTH_USER_MODEL),
     ('ovp_uploads', '0001_initial')]
    operations = [
     migrations.CreateModel(name='UploadedImage', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'image', models.ImageField(upload_to=ovp_uploads.models.ImageName(), verbose_name='Image 350x260')),
      (
       'image_small', django_resized.forms.ResizedImageField(blank=True, default=None, null=True, upload_to=ovp_uploads.models.ImageName('-small'))),
      (
       'image_medium', django_resized.forms.ResizedImageField(blank=True, default=None, null=True, upload_to=ovp_uploads.models.ImageName('-medium'))),
      (
       'image_large', django_resized.forms.ResizedImageField(blank=True, default=None, null=True, upload_to=ovp_uploads.models.ImageName('-large'))),
      (
       'created_date', models.DateTimeField(auto_now_add=True)),
      (
       'modified_date', models.DateTimeField(auto_now=True)),
      (
       'user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))], options={'verbose_name': 'uploaded image', 
      'verbose_name_plural': 'uploaded images'})]