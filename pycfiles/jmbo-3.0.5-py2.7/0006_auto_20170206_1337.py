# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0006_auto_20170206_1337.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('jmbo', '0005_modelbase_layers')]
    operations = [
     migrations.CreateModel(name=b'ImageOverride', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'replacement', models.ImageField(upload_to=b''))]),
     migrations.AlterModelOptions(name=b'image', options={b'ordering': ('title', )}),
     migrations.AddField(model_name=b'imageoverride', name=b'image', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'jmbo.Image')),
     migrations.AddField(model_name=b'imageoverride', name=b'photo_size', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'photologue.PhotoSize')),
     migrations.AlterUniqueTogether(name=b'imageoverride', unique_together=set([('image', 'photo_size')]))]