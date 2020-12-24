# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/workgroup/utils/interfaces.py
# Compiled at: 2008-06-25 09:09:13
from zope.interface import Interface

class IWorkgroupActions(Interface):
    """ WorkgroupActions utility """
    __module__ = __name__

    def disable(context):
        """ Disable workgroup action """
        pass

    def enable(context):
        """ Enable workgroup action"""
        pass