# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/captcha/browser/captchawidget.py
# Compiled at: 2008-12-22 08:23:22
"""CaptchaWidget class for the Zope 3 based ks.widget package

$Id: captchawidget.py 35233 2007-11-28 11:56:17Z anton $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 35233 $'
__date__ = '$Date: 2007-11-28 13:56:17 +0200 (Wed, 28 Nov 2007) $'
import datetime
from zope.app.form.interfaces import ConversionError, InputErrors
from zope.app.form.browser.widget import renderElement
from zope.app.form.browser import IntWidget
from ks.lib.pagetemplate.viewpagetemplatestring import ViewPageTemplateString
from ks.schema.captcha import _

class CaptchaWidget(IntWidget):
    __module__ = __name__
    imageCssClass = 'captcha'
    noImageTemplate = ''

    @property
    def keyName(self):
        return '%s.key' % self.name

    def __call__(self):
        res = []
        key = self.context.captcha.getkey()
        kwargs = {'type': 'hidden', 'name': self.keyName, 'id': self.keyName, 'value': key}
        res.append(renderElement('input', **kwargs))
        kwargs = {'src': '@@captcha?key=%s' % key, 'alt': _('Turn on images'), 'cssClass': self.imageCssClass}
        res.append(renderElement('img', **kwargs))
        res.append(super(CaptchaWidget, self).__call__())
        pt = ViewPageTemplateString(source=self.noImageTemplate)
        res.append(pt(self, self.context.context, self.request))
        return ('\n').join(res)

    def _toFieldValue(self, input):
        if self.convert_missing_value and input == self._missing:
            value = self.context.missing_value
        else:
            try:
                value = map(unicode, input)
            except ValueError, v:
                raise ConversionError(_('Incorrect text data'), v)

            if not value[0].isdigit():
                raise ConversionError(_('Random key must consist of digits!'))
            if not value[1] and not self.context.required:
                value[1] = None
                return value
            if not value[1].isdigit():
                raise ConversionError(_('Code must consist of digits!'))
            try:
                value = map(int, input)
            except ValueError, v:
                raise ConversionError(_('Data conversion error'), v)

        return value

    def _getFormInput(self):
        return (
         self.request.get(self.keyName), self.request.get(self.name))

    def _toFormValue(self, value):
        return self._missing