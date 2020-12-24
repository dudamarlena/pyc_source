# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/channel/interfaces.py
# Compiled at: 2008-12-22 07:37:15
"""Interfaces for the Zope 3 based channel package

$Id: interfaces.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.interface import Interface
from zope.schema import Tuple, ASCIILine
from ks.channel import _

class IChannel(Interface):
    __module__ = __name__

    def send(**kw):
        pass

    addresses = Tuple(title=_('Addresses'), value_type=ASCIILine(title=_('Address')), unique=True, default=())