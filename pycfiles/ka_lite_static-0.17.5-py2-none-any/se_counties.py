# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/localflavor/se/se_counties.py
# Compiled at: 2018-07-11 18:15:30
"""
An alphabetical list of Swedish counties, sorted by codes.

http://en.wikipedia.org/wiki/Counties_of_Sweden

This exists in this standalone file so that it's only imported into memory
when explicitly needed.

"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
COUNTY_CHOICES = (
 (
  b'AB', _(b'Stockholm')),
 (
  b'AC', _(b'Västerbotten')),
 (
  b'BD', _(b'Norrbotten')),
 (
  b'C', _(b'Uppsala')),
 (
  b'D', _(b'Södermanland')),
 (
  b'E', _(b'Östergötland')),
 (
  b'F', _(b'Jönköping')),
 (
  b'G', _(b'Kronoberg')),
 (
  b'H', _(b'Kalmar')),
 (
  b'I', _(b'Gotland')),
 (
  b'K', _(b'Blekinge')),
 (
  b'M', _(b'Skåne')),
 (
  b'N', _(b'Halland')),
 (
  b'O', _(b'Västra Götaland')),
 (
  b'S', _(b'Värmland')),
 (
  b'T', _(b'Örebro')),
 (
  b'U', _(b'Västmanland')),
 (
  b'W', _(b'Dalarna')),
 (
  b'X', _(b'Gävleborg')),
 (
  b'Y', _(b'Västernorrland')),
 (
  b'Z', _(b'Jämtland')))