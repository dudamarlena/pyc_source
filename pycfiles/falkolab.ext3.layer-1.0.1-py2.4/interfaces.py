# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/ext3/layer/interfaces.py
# Compiled at: 2009-06-05 02:58:05
"""
Created on 05.06.2009

@author: falko

$Id$
"""
from zope.viewlet.interfaces import IViewletManager

class IExtLayerCSS(IViewletManager):
    """CSS viewlet manager."""
    __module__ = __name__


class IExtLayerJavaScript(IViewletManager):
    """JavaScript viewlet manager."""
    __module__ = __name__