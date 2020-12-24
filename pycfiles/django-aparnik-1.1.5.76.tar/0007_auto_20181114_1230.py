# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/products/migrations/0007_auto_20181114_1230.py
# Compiled at: 2018-11-16 05:29:39
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0004_filefield_title'),
     ('products', '0006_auto_20181113_1848')]
    operations = [
     migrations.CreateModel(name=b'ProductProperty', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'title', models.CharField(max_length=100, verbose_name=b'Title')),
      (
       b'icon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'filefields.FileField', verbose_name=b'Icon'))], options={b'verbose_name': b'Product Property', 
        b'verbose_name_plural': b'Product Properties'}),
     migrations.CreateModel(name=b'ProductPropertyMembership', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'value', models.CharField(max_length=255, verbose_name=b'Content')),
      (
       b'product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'products.Product', verbose_name=b'Product')),
      (
       b'property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'products.ProductProperty', verbose_name=b'Property'))], options={b'verbose_name': b'Product Property Membership', 
        b'verbose_name_plural': b'Product Property Membership'}),
     migrations.AddField(model_name=b'product', name=b'properties', field=models.ManyToManyField(through=b'products.ProductPropertyMembership', to=b'products.ProductProperty', verbose_name=b'Product Properties'))]