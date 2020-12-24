# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucio/Projects/django-custard/custard/example/example/demo/models.py
# Compiled at: 2014-07-28 09:27:23
from django.db import models
from custard.builder import CustomFieldsBuilder
builder = CustomFieldsBuilder('demo.CustomFieldsModel', 'demo.CustomValuesModel')
CustomMixinClass = builder.create_mixin()
CustomManagerClass = builder.create_manager()

class Example(models.Model, CustomMixinClass):
    name = models.CharField(max_length=255)
    objects = CustomManagerClass()

    def __str__(self):
        return '%s' % self.name


class CustomFieldsModel(builder.create_fields()):
    pass


class CustomValuesModel(builder.create_values()):
    pass