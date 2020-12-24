# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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