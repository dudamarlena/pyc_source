# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneStatCounter\utility.py
# Compiled at: 2008-07-07 15:15:06
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from interfaces import IStatCounterConfig
from OFS.SimpleItem import SimpleItem
UTILITY_NAME = 'statcounter_config'

class StatCounterConfig(SimpleItem):
    """A local utility that stores StatCounter configuration.
    """
    __module__ = __name__
    implements(IStatCounterConfig)
    sc_project = FieldProperty(IStatCounterConfig['sc_project'])
    sc_invisible = FieldProperty(IStatCounterConfig['sc_invisible'])
    sc_partition = FieldProperty(IStatCounterConfig['sc_partition'])
    sc_security = FieldProperty(IStatCounterConfig['sc_security'])