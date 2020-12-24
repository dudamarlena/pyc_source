# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/django_galicia/forms.py
# Compiled at: 2013-01-11 11:54:06
"""
Galicia-specific Form helpers
"""
from __future__ import absolute_import, unicode_literals
from django.forms.fields import Select
from .municipalities import MUNICIPALITY_CHOICES
from .comarcas import COMARCA_CHOICES
from .provinces import PROVINCE_CHOICES

class GaliciaMunicipalitySelect(Select):
    """
    A Select widget that uses a list of Galician municipalities as its choices.
    """

    def __init__(self, attrs=None):
        super(GaliciaMunicipalitySelect, self).__init__(attrs, choices=MUNICIPALITY_CHOICES)


class GaliciaComarcaSelect(Select):
    """
    A Select widget that uses a list of Galician comarcas as its choices.
    """

    def __init__(self, attrs=None):
        super(GaliciaComarcaSelect, self).__init__(attrs, choices=COMARCA_CHOICES)


class GaliciaProvinceSelect(Select):
    """
    A Select widget that uses a list of Galician provinces as its choices.
    """

    def __init__(self, attrs=None):
        super(GaliciaProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)