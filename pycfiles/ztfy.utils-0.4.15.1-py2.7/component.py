# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/component.py
# Compiled at: 2013-12-02 04:11:37
from zope.component import getUtilitiesFor

def getRegistryNames(component, interface):
    """Get registration names of given component for given interface"""
    return [ name for name, utility in getUtilitiesFor(interface) if component is utility ]