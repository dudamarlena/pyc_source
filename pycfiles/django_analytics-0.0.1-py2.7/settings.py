# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/analytics/settings.py
# Compiled at: 2011-05-24 10:08:18
from django.utils.translation import ugettext as _
STATISTIC_FREQUENCY_DAILY = 'd'
STATISTIC_FREQUENCY_WEEKLY = 'w'
STATISTIC_FREQUENCY_MONTHLY = 'm'
STATISTIC_FREQUENCY_CHOICES = (
 (
  STATISTIC_FREQUENCY_DAILY, _('Daily')),
 (
  STATISTIC_FREQUENCY_WEEKLY, _('Weekly')),
 (
  STATISTIC_FREQUENCY_MONTHLY, _('Monthly')))
STATISTIC_FREQUENCY_DICT = dict(STATISTIC_FREQUENCY_CHOICES)
GECKOBOARD_COLOURS = [
 '666666',
 'ffcc00',
 'ff3300',
 '99cc00',
 '003300',
 '3399ff',
 '003366',
 '330066',
 '9900cc']
CSV_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
ANALYTICS_APP_MODULE = 'mod_analytics'