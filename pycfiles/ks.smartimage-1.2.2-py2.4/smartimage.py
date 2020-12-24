# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimage.py
# Compiled at: 2008-12-23 17:55:59
"""SmartImageCache class for the Zope 3 based smartimage package

$Id: smartimage.py 23811 2007-11-15 10:10:37Z anton $
"""
__author__ = 'Anton Oprya'
__license__ = 'ZPL'
__version__ = '$Revision: 23811 $'
__date__ = '$Date: 2007-11-15 12:10:37 +0200 (Thu, 15 Nov 2007) $'
from zope.interface import implements
from interfaces import ISmartImage
from zope.app.file.image import Image
from zope.app.container.contained import Contained

class SmartImage(Image, Contained):
    __module__ = __name__
    implements(ISmartImage)
    title = ''
    clearData = False

    def __init__(self, *kv, **kw):
        super(SmartImage, self).__init__(*kv, **kw)