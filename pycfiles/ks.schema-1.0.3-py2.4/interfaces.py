# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/smarturi/interfaces.py
# Compiled at: 2008-12-22 08:23:25
"""Inrefaces for the Zope 3 based smartimagecache package

$Id: interfaces.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.schema.interfaces import IObject
from zope.schema import TextLine, ASCIILine
from zope.interface import Interface
from ks.schema.smarturi import _

class IURI(Interface):
    """URI interface"""
    __module__ = __name__
    title = TextLine(title=_('URI title'), required=False)
    uri = ASCIILine(title=_('URI'))


class ISmartURI(IObject):
    """Smart URI Field"""
    __module__ = __name__