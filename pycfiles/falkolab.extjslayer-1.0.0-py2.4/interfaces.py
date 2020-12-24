# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/extjslayer/interfaces.py
# Compiled at: 2009-03-11 02:27:25
from zope.publisher.interfaces.browser import IBrowserRequest

class IExtJSLayer(IBrowserRequest):
    """  extjs layer  """
    __module__ = __name__


class IExtJSDebugLayer(IExtJSLayer):
    """  extjs debug layer  """
    __module__ = __name__