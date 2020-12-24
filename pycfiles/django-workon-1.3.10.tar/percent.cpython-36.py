# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/PACKAGES/WORKON/workon/fields/percent.py
# Compiled at: 2018-03-15 02:43:44
# Size of source mod 2**32: 665 bytes
from django.db import models
from django import forms
from django.utils.text import capfirst
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
__all__ = [
 'PercentField']

class PercentField(models.PositiveIntegerField):
    __doc__ = '\n    Positive integer with percent validators\n    '

    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [MaxValueValidator(100), MinValueValidator(0)]
        (super().__init__)(*args, **kwargs)