# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimageschema/interfaces.py
# Compiled at: 2008-12-23 17:55:58
"""Inrefaces for the Zope 3 based smartimagecache package

$Id: interfaces.py 35338 2008-06-12 18:42:18Z anatoly $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 35338 $'
__date__ = '$Date: 2008-06-12 21:42:18 +0300 (Thu, 12 Jun 2008) $'
from zope.schema.interfaces import IObject
from zope.schema import TextLine
from zope.interface import Interface

class ISmartImageField(IObject):
    """Smart Image Field"""
    __module__ = __name__
    scale = TextLine()


class ISmartImageParent(Interface):
    """Smart Image Parent"""
    __module__ = __name__