# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/enums.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 1107 bytes
from __future__ import absolute_import
from django.utils.translation import ugettext_lazy
OPERATOR_UNKNOWN = 0
OPERATOR_PROXIMUS = 1
OPERATOR_MOBISTAR = 2
OPERATOR_BASE = 3
OPERATOR_OTHER = 999
OPERATOR_CHOICES = (
 (
  OPERATOR_UNKNOWN, ugettext_lazy('Unknown')),
 (
  OPERATOR_PROXIMUS, 'Proximus'),
 (
  OPERATOR_MOBISTAR, 'Mobistar'),
 (
  OPERATOR_BASE, 'Base'),
 (
  OPERATOR_OTHER, ugettext_lazy('Other')))
GATEWAY_MOBILEWEB = 1
GATEWAY_SMSEXTRAPRO = 3
GATEWAY_SPRYNG = 4
GATEWAY_CHOICES = (
 (
  GATEWAY_MOBILEWEB, 'MobileWeb'),
 (
  GATEWAY_SMSEXTRAPRO, 'SmsExtraPro'),
 (
  GATEWAY_SPRYNG, 'Spryng'))
DIRECTION_BOTH = 2
DIRECTION_INBOUND = 1
DIRECTION_OUTBOUND = 0
DIRECTION_CHOICES = (
 (
  DIRECTION_BOTH, ugettext_lazy('Both')),
 (
  DIRECTION_INBOUND, ugettext_lazy('Inbound')),
 (
  DIRECTION_OUTBOUND, ugettext_lazy('Outbound')))
PRIORITY_HIGH = '1'
PRIORITY_MEDIUM = '2'
PRIORITY_LOW = '3'
PRIORITY_DEFERRED = '9'
PRIORITIES = (
 (
  PRIORITY_HIGH, 'high'),
 (
  PRIORITY_MEDIUM, 'medium'),
 (
  PRIORITY_LOW, 'low'),
 (
  PRIORITY_DEFERRED, 'deferred'))