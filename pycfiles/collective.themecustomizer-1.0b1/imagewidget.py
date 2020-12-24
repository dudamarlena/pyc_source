# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/themecustomizer/src/collective/themecustomizer/browser/imagewidget.py
# Compiled at: 2014-01-06 13:09:25
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib.textwidgets import FileWidget

class ImageWidget(FileWidget):
    """Custom implementation of ImageWidget
    """
    template = ViewPageTemplateFile('templates/imagewidget.pt')
    displayWidth = 30

    def __call__(self):
        value = self._getFormValue() or None
        return self.template(name=self.context.__name__, value=value)

    def _toFieldValue(self, input):
        action = self.request.get('%s.action' % self.name, None)
        if action == 'remove':
            return 'remove'
        else:
            value = super(ImageWidget, self)._toFieldValue(input)
            return value

    def hasInput(self):
        return (self.name + '.used' in self.request.form or self.name in self.request.form) and not self.request.form.get(self.name + '.nochange', '')