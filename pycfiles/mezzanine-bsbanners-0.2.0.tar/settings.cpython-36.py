# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/settings.py
# Compiled at: 2018-11-16 08:16:10
# Size of source mod 2**32: 422 bytes
"""
Settings for Mezzanine BS Banners
"""
from django.conf import settings
MEDIA = getattr(settings, 'BSBANNERS_MEDIA', 'slides/')