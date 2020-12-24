# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/config.py
# Compiled at: 2015-11-03 03:53:19
from bika.lims.config import *
from Products.Archetypes.public import DisplayList
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from bika.health.permissions import *
PROJECTNAME = 'bika.health'
GENDERS = DisplayList((
 (
  'male', _('Male')),
 (
  'female', _('Female')),
 (
  'dk', _("Don't Know"))))
ETHNICITIES = DisplayList((
 (
  'Native American', _('Native American')),
 (
  'Asian', _('Asian')),
 (
  'Black', _('Black')),
 (
  'Native Hawaiian or Other Pacific Islander', _('Native Hawaiian or Other Pacific Islander')),
 (
  'White', _('White')),
 (
  'Hispanic or Latino', _('Hispanic or Latino'))))
GENDERS_APPLY = DisplayList((
 (
  'male', _('Male')),
 (
  'female', _('Female')),
 (
  'dk', _('Both'))))
MENSTRUAL_STATUSES = DisplayList((
 (
  'regular', _('Regular')),
 (
  'irregular', _('Irregular')),
 (
  'none', _('No menstrual cycle'))))
EMAIL_SUBJECT_OPTIONS.add('health.cp', _('Client PID'))