# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/image/browser/imagedisplaywidget.py
# Compiled at: 2008-12-22 08:23:20
"""ImageDisplayWidget class for the Zope 3 based ks.widget package

$Id: imagedisplaywidget.py 35321 2008-01-07 22:03:46Z cray $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 35321 $'
__date__ = '$Date: 2008-01-08 00:03:46 +0200 (Tue, 08 Jan 2008) $'
from zope.interface import implements
from zope.traversing.browser import absoluteURL
from zope.app.form.interfaces import IDisplayWidget
from zope.app.form.browser.widget import DisplayWidget, renderElement

class ImageDisplayWidget(DisplayWidget):
    __module__ = __name__
    implements(IDisplayWidget)
    cssClass = ''
    extra = ''

    def __call__(self):
        src = '%s/++attribute++%s/++attribute++__call__' % (absoluteURL(self.context.context, self.request), self.context.__name__)
        return renderElement('img', src=src, cssClass=self.cssClass, extra=self.extra)