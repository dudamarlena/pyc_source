# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sf_www/mezzanine/personal/heroku/personal/portfolio/migrations/0002_portfolioimage.py
# Compiled at: 2016-12-25 14:17:39
# Size of source mod 2**32: 1444 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, mezzanine.core.fields

class Migration(migrations.Migration):
    dependencies = [
     ('portfolio', '0001_initial')]
    operations = [
     migrations.CreateModel(name='PortfolioImage', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       '_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
      (
       'file', mezzanine.core.fields.FileField(max_length=200, verbose_name='File')),
      (
       'description', models.CharField(blank=True, max_length=1000, verbose_name='Description')),
      (
       'description_en', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Description')),
      (
       'description_ru', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Description')),
      (
       'portfolio_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='portfolio.PortfolioPost'))], options={'ordering': ('_order', ), 
      'verbose_name': 'Image', 
      'verbose_name_plural': 'Images'})]