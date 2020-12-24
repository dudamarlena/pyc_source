# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/erp.juanmitaboada.com/codenerix_reviews/migrations/0001_initial.py
# Compiled at: 2018-05-26 03:03:48
# Size of source mod 2**32: 1828 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('codenerix_products', '0012_productunique_caducity'),
     ('codenerix_invoicing', '0020_auto_20180515_1333')]
    operations = [
     migrations.CreateModel(name='Reviews', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'stars', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Stars')),
      (
       'reviews', models.TextField(verbose_name='Reviews')),
      (
       'validate', models.BooleanField(default=False, verbose_name='Validate')),
      (
       'lang', models.CharField(choices=[('es', 'Spanish')], max_length=2, verbose_name='Language')),
      (
       'customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='codenerix_invoicing.Customer', verbose_name='Customer')),
      (
       'product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='codenerix_products.ProductFinal', verbose_name='Product'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')})]