# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_looking_glass/apps.py
# Compiled at: 2015-11-10 08:14:09
# Size of source mod 2**32: 293 bytes
"""
App configuration
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DHCPKitLookingGlassConfig(AppConfig):
    __doc__ = '\n    DHCPKit Looking Glass config\n    '
    name = 'dhcpkit_looking_glass'
    verbose_name = _('DHCPKit Looking Glass')