# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/timezone/utility.py
# Compiled at: 2012-06-20 10:07:04
__docformat__ = 'restructuredtext'
from persistent import Persistent
from ztfy.utils.timezone.interfaces import IServerTimezone
from zope.container.contained import Contained
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

class ServerTimezoneUtility(Persistent, Contained):
    implements(IServerTimezone)
    timezone = FieldProperty(IServerTimezone['timezone'])