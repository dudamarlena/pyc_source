# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/interfaces/timezone.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 994 bytes
__doc__ = 'PyAMS_utils.interfaces.timezone module\n\nThis module provides timezone utility interface and schema field\n'
from zope.interface import Interface
from pyams_utils.schema import TimezoneField
__docformat__ = 'restructuredtext'
from pyams_utils import _

class IServerTimezone(Interface):
    """IServerTimezone"""
    timezone = TimezoneField(title=_('Server timezone'), description=_('Default server timezone'), required=True)