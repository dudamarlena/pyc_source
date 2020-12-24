# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/geoportal/utility.py
# Compiled at: 2013-02-25 10:55:36
from persistent import Persistent
from zope.container.contained import Contained
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.geoportal.interfaces import IGeoportalConfigurationUtility

class GeoportalConfigurationUtility(Persistent, Contained):
    """Geoportal configuration utility"""
    implements(IGeoportalConfigurationUtility)
    api_key = FieldProperty(IGeoportalConfigurationUtility['api_key'])
    version = FieldProperty(IGeoportalConfigurationUtility['version'])
    development = FieldProperty(IGeoportalConfigurationUtility['development'])