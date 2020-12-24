# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/timezone/utility.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 981 bytes
"""PyAMS_utils.timezone.utility module

"""
from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty
from pyams_utils.interfaces.timezone import IServerTimezone
__docformat__ = 'restructuredtext'

@implementer(IServerTimezone)
class ServerTimezoneUtility(Persistent, Contained):
    __doc__ = 'Server timezone utility'
    timezone = FieldProperty(IServerTimezone['timezone'])