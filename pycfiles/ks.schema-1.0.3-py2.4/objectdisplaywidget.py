# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/object/browser/objectdisplaywidget.py
# Compiled at: 2008-12-22 08:23:25
"""ObjectDisplayWidget class for the Zope 3 based ks.widget package

$Id: objectdisplaywidget.py 35321 2008-01-07 22:03:46Z cray $
"""
__author__ = 'Anatoly Zaretsky'
__license__ = 'ZPL'
__version__ = '$Revision: 35321 $'
__date__ = '$Date: 2008-01-08 00:03:46 +0200 (Tue, 08 Jan 2008) $'
__credits__ = 'Based heavily on zope.app.form.browser.objectwidget.ObjectWidget'
from zope.interface import implements
from zope.schema import getFieldNamesInOrder
from zope.app.form.interfaces import IDisplayWidget
from zope.app.form.utility import setUpWidgets
from zope.app.form.browser.widget import DisplayWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

class ObjectDisplayWidgetView(object):
    __module__ = __name__
    template = ViewPageTemplateFile('objectdisplaywidget.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()


class ObjectDisplayWidget(DisplayWidget):
    __module__ = __name__
    implements(IDisplayWidget)
    names = None
    viewFactory = ObjectDisplayWidgetView

    def __init__(self, context, request, **kw):
        super(ObjectDisplayWidget, self).__init__(context, request)
        self.view = self.viewFactory(self, request)
        if self.names is None:
            self.names = getFieldNamesInOrder(self.context.schema)
        for (k, v) in kw.items():
            if k.endswith('_widget'):
                setattr(self, k, v)

        self._setUpWidgets()
        return

    def setPrefix(self, prefix):
        super(ObjectDisplayWidget, self).setPrefix(prefix)
        self._setUpWidgets()

    def _setUpWidgets(self):
        setUpWidgets(self, self.context.schema, IDisplayWidget, prefix=self.name, names=self.names, context=self.context)

    def __call__(self):
        return self.view()

    def legendTitle(self):
        return self.context.title or self.context.__name__

    def getSubWidget(self, name):
        return getattr(self, '%s_widget' % name)

    def subwidgets(self):
        return [ self.getSubWidget(name) for name in self.names ]

    def hidden(self):
        """Render the object as hidden fields."""
        result = []
        for name in self.names:
            result.append(getSubwidget(name).hidden())

        return ('').join(result)

    def setRenderedValue(self, value):
        """Set the default data for the widget.

        The given value should be used even if the user has entered
        data.
        """
        self._setUpWidgets()
        for name in self.names:
            self.getSubWidget(name).setRenderedValue(getattr(value, name, None))

        return