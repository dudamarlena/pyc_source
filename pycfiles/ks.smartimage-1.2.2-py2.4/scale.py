# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimagecache/scale.py
# Compiled at: 2008-12-23 17:55:59
"""SmartImageCache class for the Zope 3 based smartimage package

$Id: scale.py 12472 2007-10-26 19:21:11Z anton $
"""
__author__ = 'Andrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 12472 $'
__date__ = '$Date: 2007-10-26 22:21:11 +0300 (Fri, 26 Oct 2007) $'
from zope.interface import implements
from interfaces import IScale

class Scale(object):
    __module__ = __name__
    implements(IScale)
    name = ''
    width = 100
    height = 100

    def __init__(self, name='', width=100, height=100, *kv, **kw):
        super(Scale, self).__init__(self, *kv, **kw)
        self.name = name
        self.width = width
        self.height = height