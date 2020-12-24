# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/arpamynt/mezzanine_faq/migrations/0001_initial.py
# Compiled at: 2016-01-12 18:39:38
from __future__ import unicode_literals
from django.db import migrations, models
import mezzanine.core.fields

class Migration(migrations.Migration):
    dependencies = [
     ('pages', '0004_page_featured_image')]
    operations = [
     migrations.CreateModel(name=b'FaqPage', fields=[
      (
       b'page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=b'pages.Page'))], options={b'ordering': ('_order', ), 
        b'verbose_name': b'FAQ', 
        b'verbose_name_plural': b'FAQ'}, bases=('pages.page', )),
     migrations.CreateModel(name=b'FaqQuestion', fields=[
      (
       b'id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
      (
       b'_order', mezzanine.core.fields.OrderField(null=True, verbose_name=b'Order')),
      (
       b'question', models.TextField(verbose_name=b'Question')),
      (
       b'answer', models.TextField(verbose_name=b'Answer')),
      (
       b'page', models.ForeignKey(to=b'mezzanine_faq.FaqPage'))], options={b'ordering': ('_order', ), 
        b'verbose_name': b'Question', 
        b'verbose_name_plural': b'Questions'})]