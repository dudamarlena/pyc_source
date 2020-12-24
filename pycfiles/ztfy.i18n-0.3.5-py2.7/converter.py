# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/browser/widget/converter.py
# Compiled at: 2012-06-20 11:46:34
from z3c.form.interfaces import IWidget, NOT_CHANGED
from z3c.language.switch.interfaces import II18n
from ztfy.i18n.interfaces import II18nField, II18nFileField
from z3c.form.converter import BaseDataConverter, FieldWidgetDataConverter
from zope.component import adapts

class I18nFieldDataConverter(BaseDataConverter):
    """Base data converter for I18n fields"""
    adapts(II18nField, IWidget)

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        result = {}
        langs = self.widget.langs
        for index, lang in enumerate(langs):
            converter = FieldWidgetDataConverter(self.widget.widgets[lang])
            result[lang] = converter.toFieldValue(value[index])

        return result


class I18nFileFieldDataConverter(I18nFieldDataConverter):
    """File data converter for I18n fields"""
    adapts(II18nFileField, IWidget)

    def toFieldValue(self, value):
        result = {}
        langs = self.widget.langs
        for index, lang in enumerate(langs):
            widget = self.widget.widgets[lang]
            if widget.deleted:
                result[lang] = None
            else:
                converter = FieldWidgetDataConverter(widget)
                field_value = converter.toFieldValue(value[index])
                if isinstance(field_value, tuple) and field_value[0] is NOT_CHANGED:
                    field_value = field_value[0]
                if field_value:
                    result[lang] = field_value
                elif not widget.ignoreContext:
                    result[lang] = II18n(self.widget.context).getAttribute(self.widget.field.getName(), language=lang)
                else:
                    result[lang] = None

        return result