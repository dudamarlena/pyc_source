# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/qvit/Django/torex/color_captcha/settings.py
# Compiled at: 2013-08-20 13:05:13
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils import check_colors
DEFAULT_COLORS = [
 (
  'white', _('white')),
 (
  'blue', _('blue')),
 (
  'red', _('red'))]
COLORS = getattr(settings, 'CAPTCHA_COLORS', DEFAULT_COLORS)
check_colors(COLORS)