# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/html/browser/htmldisplaywidget.py
# Compiled at: 2008-12-22 08:23:24
"""HTMLDisplayWidget class for the Zope 3 based ks.widget package

$Id: htmldisplaywidget.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
__credits__ = 'Based heavily on zope.app.form.browser.objectwidget.ObjectWidget'
from zope.app.form.interfaces import IDisplayWidget
from zope.app.form.browser.widget import DisplayWidget, UnicodeDisplayWidget
from zope.interface import implements
from ks.schema.html import _

class UnicodeHTMLDisplayWidget(UnicodeDisplayWidget):
    __module__ = __name__
    implements(IDisplayWidget)

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return ''
        return unicode(value)


class HTMLDisplayWidget(DisplayWidget):
    __module__ = __name__
    implements(IDisplayWidget)

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return ''
        return value