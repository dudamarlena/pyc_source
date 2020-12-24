# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/widget/textarea.py
# Compiled at: 2012-06-20 11:46:34
from z3c.form.interfaces import IFieldWidget
from ztfy.i18n.browser.widget.interfaces import II18nTextAreaWidget
from ztfy.i18n.interfaces import II18nTextField
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementsOnly, implementer
from ztfy.i18n.browser.widget.widget import I18nWidget, I18nWidgetProperty

class I18nTextAreaWidget(I18nWidget, TextAreaWidget):
    """I18n text input type implementation"""
    implementsOnly(II18nTextAreaWidget)
    original_widget = TextAreaWidget
    rows = I18nWidgetProperty('rows')
    cols = I18nWidgetProperty('cols')
    readonly = I18nWidgetProperty('readonly')
    onselect = I18nWidgetProperty('onselect')


@adapter(II18nTextField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def I18nTextAreaFieldWidget(field, request):
    """IFieldWidget factory for I18nTextWidget"""
    return FieldWidget(field, I18nTextAreaWidget(request))