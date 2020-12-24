# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/browser/widget.py
# Compiled at: 2009-04-26 22:17:24
from zope.component import getMultiAdapter, getUtility
from zope.app.form.interfaces import IInputWidget
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.DigestoContentTypes.utilities.interfaces import INormativaTypes

class DynamicSequenceWidget(SimpleInputWidget):
    __module__ = __name__
    __call__ = ViewPageTemplateFile('templates/widget.pt')

    def _getFormInput(self):
        value = super(DynamicSequenceWidget, self)._getFormInput()
        if value is None:
            value = []
        if not isinstance(value, list):
            value = [
             value]
        return value

    def hasInput(self):
        return self.name + '.marker' in self.request.form

    def hidden(self):
        s = ''
        for value in self._getFormValue():
            widget = getMultiAdapter((self.context.value_type, self.request), IInputWidget)
            widget.name = self.name
            widget.setRenderedValue(value)
            s += widget.hidden()

        return s


class NormativaDynamicSequenceWidget(DynamicSequenceWidget):
    __module__ = __name__

    def _getFormValue(self):
        cu = getUtility(INormativaTypes)
        return cu.types