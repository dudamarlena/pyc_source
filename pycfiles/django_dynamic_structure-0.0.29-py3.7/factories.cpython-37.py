# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dyn_struct/factories.py
# Compiled at: 2017-12-05 22:57:16
# Size of source mod 2**32: 779 bytes
import factory, factory.fuzzy
from .db import models
FORM_FIELD_CHOICES = [
 'CharField', 'IntegerField', 'DateField', 'EmailField', 'BooleanField']

class DynamicStructure(factory.django.DjangoModelFactory):

    class Meta:
        model = models.DynamicStructure

    name = factory.fuzzy.FuzzyText(length=10, prefix='test_dyn_struct_')


class DynamicStructureField(factory.django.DjangoModelFactory):

    class Meta:
        model = models.DynamicStructureField

    header = factory.fuzzy.FuzzyText(length=10, prefix='test_header_field_')
    name = factory.fuzzy.FuzzyText(length=10, prefix='test_name_field_')
    form_field = factory.fuzzy.FuzzyChoice(FORM_FIELD_CHOICES)
    row = factory.fuzzy.FuzzyInteger(0, 5)
    position = factory.fuzzy.FuzzyInteger(0, 10)