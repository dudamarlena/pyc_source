# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/interfaces/timezone.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 994 bytes
"""PyAMS_utils.interfaces.timezone module

This module provides timezone utility interface and schema field
"""
from zope.interface import Interface
from pyams_utils.schema import TimezoneField
__docformat__ = 'restructuredtext'
from pyams_utils import _

class IServerTimezone(Interface):
    __doc__ = 'Server timezone interface'
    timezone = TimezoneField(title=_('Server timezone'), description=_('Default server timezone'), required=True)