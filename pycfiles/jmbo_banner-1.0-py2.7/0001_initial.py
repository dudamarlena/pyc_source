# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/migrations/0001_initial.py
# Compiled at: 2018-01-09 13:54:21
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion, simplemde.fields, sortedm2m.fields
from banner.styles import BANNER_STYLE_CLASSES

def styles():
    return [ (klass.__name__, klass.__name__) for klass in BANNER_STYLE_CLASSES
           ]


class Migration(migrations.Migration):
    initial = True
    dependencies = [
     ('jmbo', '0007_auto_20170314_1546'),
     ('link', '0002_auto_20160902_0249')]
    operations = [
     migrations.CreateModel(name=b'Banner', fields=[
      (
       b'modelbase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=b'jmbo.ModelBase')),
      (
       b'style', models.CharField(choices=styles(), default=b'BaseStyle', max_length=128)),
      (
       b'headline', simplemde.fields.SimpleMDEField(blank=True, help_text=b"The banner's headline.", null=True)),
      (
       b'body', simplemde.fields.SimpleMDEField(blank=True, help_text=b"The banner's main text content.", null=True)),
      (
       b'link', models.ForeignKey(blank=True, help_text=b'Link to which this banner should redirect.', null=True, on_delete=django.db.models.deletion.CASCADE, to=b'link.Link'))], bases=('jmbo.modelbase', )),
     migrations.CreateModel(name=b'Button', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'text', models.CharField(help_text=b'The text to be displayed as the button label', max_length=60)),
      (
       b'banner', sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, null=True, related_name=b'buttons', to=b'banner.Banner')),
      (
       b'link', models.ForeignKey(blank=True, help_text=b'CTA link for this button', null=True, on_delete=django.db.models.deletion.CASCADE, to=b'link.Link'))])]