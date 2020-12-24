# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/widget/text.py
# Compiled at: 2012-06-20 11:46:34
from z3c.form.interfaces import IFieldWidget
from ztfy.i18n.browser.widget.interfaces import II18nTextWidget
from ztfy.i18n.interfaces import II18nTextLineField
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget
from zope.component import adapter
from zope.interface import implementsOnly, implementer
from ztfy.i18n.browser.widget.widget import I18nWidget, I18nWidgetProperty

class I18nTextWidget(I18nWidget, TextWidget):
    """I18n text input type implementation"""
    implementsOnly(II18nTextWidget)
    original_widget = TextWidget
    maxlength = I18nWidgetProperty('maxlength')
    size = I18nWidgetProperty('size')

    def updateWidget(self, widget, language):
        super(I18nTextWidget, self).updateWidget(widget, language)
        widget.maxlength = widget.field.max_length


@adapter(II18nTextLineField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def I18nTextFieldWidget(field, request):
    """IFieldWidget factory for I18nTextWidget"""
    return FieldWidget(field, I18nTextWidget(request))