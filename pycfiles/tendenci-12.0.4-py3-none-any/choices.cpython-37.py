# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/directories/choices.py
# Compiled at: 2020-02-26 14:47:57
# Size of source mod 2**32: 692 bytes
import django.utils.translation as _
DURATION_CHOICES = (
 (
  14, _('14 Days from Activation date')),
 (
  60, _('60 Days from Activation date')),
 (
  90, _('90 Days from Activation date')),
 (
  120, _('120 Days from Activation date')),
 (
  365, _('1 Year from Activation date')))
ADMIN_DURATION_CHOICES = (
 (
  0, _('Unlimited')),
 (
  14, _('14 Days from Activation date')),
 (
  30, _('30 Days from Activation date')),
 (
  60, _('60 Days from Activation date')),
 (
  90, _('90 Days from Activation date')),
 (
  120, _('120 Days from Activation date')),
 (
  365, _('1 Year from Activation date')))
STATUS_CHOICES = (
 (
  1, _('Active')),
 (
  0, _('Inactive')))