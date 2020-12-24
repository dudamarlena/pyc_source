# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/widget/file.py
# Compiled at: 2012-06-20 11:46:34
from z3c.form.interfaces import IFieldWidget, NOT_CHANGED
from ztfy.i18n.browser.widget.interfaces import II18nFileWidget
from ztfy.i18n.interfaces import II18nFileField
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer, implementsOnly
from ztfy.file.browser.widget import FileWidget
from ztfy.i18n.browser.widget.widget import I18nWidget, I18nWidgetProperty

class I18nFileWidget(I18nWidget, FileWidget):
    """I18n text input type implementation"""
    implementsOnly(II18nFileWidget)
    original_widget = FileWidget
    headers = I18nWidgetProperty('headers')
    filename = I18nWidgetProperty('filename')

    @property
    def current_value(self):
        if self.form.ignoreContext:
            return {}
        return self.field.get(self.context)

    def hasValue(self, language):
        value = self.getValue(language)
        if value is NOT_CHANGED:
            return bool(self.current_value.get(language))
        else:
            return bool(value)

    def deletable(self, language):
        if self.required:
            return False
        return self.hasValue(language)


@adapter(II18nFileField, IZTFYBrowserLayer)
@implementer(IFieldWidget)
def I18nFileFieldWidget(field, request):
    """IFieldWidget factory for I18nFileWidget"""
    return FieldWidget(field, I18nFileWidget(request))