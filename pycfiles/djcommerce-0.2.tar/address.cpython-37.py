# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\jeff\Desktop\CodingDojoPractice\CodingDojoWork\python_stack\django\Django_Commerce\django_commerce\djcommerce\models\address.py
# Compiled at: 2019-06-27 23:16:34
# Size of source mod 2**32: 662 bytes
from django.db import models
from django.conf import settings
from localflavor.us.models import USStateField, USZipCodeField

class Address(models.Model):
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = USStateField()
    zip = USZipCodeField()

    def __str__(self):
        return '{}{},{},{}{}'.format(self.address_line_1, self.address_line_2, self.city, self.state, self.zip)

    class Meta:
        abstract = False
        if hasattr(settings, 'ADDRESS_MODEL'):
            abstract = True