# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/timezone/utility.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 981 bytes
__doc__ = 'PyAMS_utils.timezone.utility module\n\n'
from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from pyams_utils.interfaces.timezone import IServerTimezone
__docformat__ = 'restructuredtext'

@implementer(IServerTimezone)
class ServerTimezoneUtility(Persistent, Contained):
    """ServerTimezoneUtility"""
    timezone = FieldProperty(IServerTimezone['timezone'])