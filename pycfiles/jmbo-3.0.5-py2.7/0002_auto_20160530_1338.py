# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/migrations/0002_auto_20160530_1338.py
# Compiled at: 2017-05-03 05:57:29
from __future__ import unicode_literals
import os
from django.db import migrations
from django.core.files.base import ContentFile

def create_images(apps, schema_editor):
    ModelBase = apps.get_model(b'jmbo', b'ModelBase')
    Image = apps.get_model(b'jmbo', b'Image')
    ModelBaseImage = apps.get_model(b'jmbo', b'ModelBaseImage')
    for obj in ModelBase.objects.all():
        if obj.image:
            image = Image.objects.create(title=b'Canonical image', subtitle=b'For #%s' % obj.pk)
            image.image.save(os.path.basename(obj.image.path), ContentFile(open(obj.image.path, b'rb').read()))
            ModelBaseImage.objects.create(modelbase=obj, image=image)


class Migration(migrations.Migration):
    dependencies = [
     ('jmbo', '0001_initial')]
    operations = [
     migrations.RunPython(create_images)]