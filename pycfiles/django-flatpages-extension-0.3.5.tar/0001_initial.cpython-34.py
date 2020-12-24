# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django-flatpages-extension/django-flatpages-extension/migrations/0001_initial.py
# Compiled at: 2018-07-10 12:52:03
# Size of source mod 2**32: 969 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('flatpages', '0001_initial')]
    operations = [
     migrations.CreateModel(name='FlatPageExtended', fields=[
      (
       'flatpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
      (
       'meta_title', models.CharField(blank=True, max_length=500, null=True, verbose_name='Title')),
      (
       'meta_keywords', models.CharField(blank=True, max_length=500, null=True, verbose_name='Keywords')),
      (
       'meta_description', models.TextField(blank=True, null=True, verbose_name='Description'))], bases=('flatpages.flatpage', ))]