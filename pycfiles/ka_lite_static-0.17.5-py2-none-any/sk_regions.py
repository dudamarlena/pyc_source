# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/localflavor/sk/sk_regions.py
# Compiled at: 2018-07-11 18:15:30
"""
Slovak regions according to http://sk.wikipedia.org/wiki/Administrat%C3%ADvne_%C4%8Dlenenie_Slovenska
"""
from django.utils.translation import ugettext_lazy as _
REGION_CHOICES = (
 (
  'BB', _('Banska Bystrica region')),
 (
  'BA', _('Bratislava region')),
 (
  'KE', _('Kosice region')),
 (
  'NR', _('Nitra region')),
 (
  'PO', _('Presov region')),
 (
  'TN', _('Trencin region')),
 (
  'TT', _('Trnava region')),
 (
  'ZA', _('Zilina region')))