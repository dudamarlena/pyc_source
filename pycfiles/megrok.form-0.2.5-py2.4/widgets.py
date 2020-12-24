# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/megrok/form/widgets.py
# Compiled at: 2008-04-23 23:50:41
from zope.app.form.browser.widget import DisplayWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

class TinyDisplayWidget(DisplayWidget):
    __module__ = __name__
    template = ViewPageTemplateFile('tinydisplaywidget.pt')

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = ''
        return self.template(name=self.context.__name__, value=value)