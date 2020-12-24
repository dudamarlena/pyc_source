# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/guestlist/constants.py
# Compiled at: 2019-04-03 22:56:31
# Size of source mod 2**32: 671 bytes
from django.utils.translation import ugettext_lazy as _
GUESTLIST_ADMISSION_CHOICES = [
 (
  'Always', _('Always added to guest list')),
 (
  'EventOnly', _('Add if the person is a staff member for this event')),
 (
  'Day', _('Add if the person is a staff member on that day')),
 (
  'Week', _('Add if the person is a staff member in that week')),
 (
  'Month', _('Add if the person is a staff member in that month')),
 (
  'Year', _('Add if the person is a staff member in that year'))]
GUESTLIST_SORT_CHOICES = [
 (
  'Last', _('Last name (default)')),
 (
  'First', _('First name')),
 (
  'Comp', _('Admission type (e.g. staff, registrant, other'))]