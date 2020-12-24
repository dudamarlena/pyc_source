# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/src/sensei2/sensei2/sensei/handlers/files.py
# Compiled at: 2015-10-21 14:10:28
from cStringIO import StringIO
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image
from random import randint, choice
from sensei2.sensei.handlers.base import BaseHandler

class ImageFieldHandler(BaseHandler):

    def __init__(self):
        super(ImageFieldHandler, self).__init__()
        self.handled_class = models.ImageField

    def object_mode(self, obj, field, sensei):
        width = randint(100, 200)
        height = randint(100, 200)
        image = Image.new('RGBA', (width, height), (
         choice((randint(0, 51), randint(102, 153), randint(204, 255))),
         choice((randint(0, 51), randint(102, 153), randint(204, 255))),
         choice((randint(0, 51), randint(102, 153), randint(204, 255)))))
        i = StringIO()
        image.save(i, format='png')
        getattr(obj, field.attname).save('sensei_image.png', ContentFile(i.getvalue()), save=False)


class FileFieldHandler(ImageFieldHandler):

    def __init__(self):
        super(FileFieldHandler, self).__init__()
        self.handled_class = models.FileField