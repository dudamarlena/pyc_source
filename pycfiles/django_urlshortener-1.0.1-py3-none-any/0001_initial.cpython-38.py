# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\urlshortener\src\urlshortener\migrations\0001_initial.py
# Compiled at: 2020-05-02 22:40:46
# Size of source mod 2**32: 1381 bytes
from django.db import migrations, models
import urlshortener.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
     migrations.CreateModel(name='URLShortenerModel',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'title', models.CharField(blank=True, max_length=60, null=True)),
      (
       'description', models.CharField(blank=True, max_length=160, null=True)),
      (
       'image', models.ImageField(blank=True, null=True, upload_to='')),
      (
       'url', models.URLField()),
      (
       'slug', models.CharField(max_length=5, unique=True, validators=[urlshortener.validators.shortcode_not_allowed])),
      (
       'status', models.CharField(choices=[('ACTIVE', 'active'), ('DEACTIVE', 'deactive')], default='active', max_length=8)),
      (
       'created_at', models.DateTimeField(auto_now=True)),
      (
       'updated_at', models.DateTimeField(auto_now_add=True))],
       options={'verbose_name':'Shortener', 
      'verbose_name_plural':'Shorteners', 
      'ordering':[
       '-pk']})]