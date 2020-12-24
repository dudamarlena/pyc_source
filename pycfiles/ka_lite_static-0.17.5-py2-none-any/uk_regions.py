# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/localflavor/uk/uk_regions.py
# Compiled at: 2018-07-11 18:15:30
from django.contrib.localflavor.gb.gb_regions import ENGLAND_REGION_CHOICES, NORTHERN_IRELAND_REGION_CHOICES, WALES_REGION_CHOICES, SCOTTISH_REGION_CHOICES, GB_NATIONS_CHOICES, GB_REGION_CHOICES
import warnings
warnings.warn('The "UK" prefix for United Kingdom has been deprecated in favour of the GB code. Please use the new GB-prefixed names.', DeprecationWarning)
UK_NATIONS_CHOICES = GB_NATIONS_CHOICES
UK_REGION_CHOICES = GB_REGION_CHOICES