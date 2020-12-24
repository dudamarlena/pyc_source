# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/migrations/0009_auto_20180918_1143.py
# Compiled at: 2018-09-18 07:43:04
# Size of source mod 2**32: 970 bytes
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('reader', '0008_attachment')]
    operations = [
     migrations.CreateModel(name='Board',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=100)),
      (
       'tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=40), blank=True, default=list, size=100)),
      (
       'reader', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='reader.ReaderProfile'))]),
     migrations.AlterUniqueTogether(name='board',
       unique_together={
      ('name', 'reader')})]