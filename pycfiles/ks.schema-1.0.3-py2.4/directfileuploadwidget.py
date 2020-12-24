# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/bytes/browser/directfileuploadwidget.py
# Compiled at: 2008-12-22 08:23:20
from zope.app.form.browser import FileWidget
from xml.sax.saxutils import quoteattr, escape
import zope.i18nmessageid
_ = zope.i18nmessageid.MessageFactory('zope')

class DirectFileUploadWidget(FileWidget):
    """File Widget"""
    __module__ = __name__

    def _toFieldValue(self, input):
        if input is None or input == '':
            return self.context.missing_value
        try:
            seek = input.seek
            read = input.read
        except AttributeError, e:
            raise ConversionError(_('Form input is not a file object'), e)
        else:
            if read or getattr(input, 'filename', ''):
                return input
            else:
                return self.context.missing_value

        return

    def _toFormValue(self, value):
        return 'File'

    def hasInput(self):
        return self.name + '.used' in self.request.form or self.name in self.request.form