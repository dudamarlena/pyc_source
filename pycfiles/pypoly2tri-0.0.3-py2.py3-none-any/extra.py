# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/webpage/form/extra.py
# Compiled at: 2011-09-13 05:11:04
import re, types, pypoly
from pypoly.content.webpage import ContentType
from pypoly.content.webpage.table import ContentCell
from pypoly.content.webpage.form import FormObject

class FormTable(FormObject):
    """
    Test
    """
    type = ContentType('extra.formtable')

    def __init__(self, name, **options):
        FormObject.__init__(self, name, **options)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        if type(value) == types.StringType or type(value) == types.UnicodeType:
            self.raw_value = value
        else:
            self.raw_value = str(value)

    value = property(_get_value, _set_value)

    def validate(self):
        errors = []
        for row in self.value:
            for cell in row:
                if type(cell) == ContentCell:
                    errors = errors + cell.value.validate()

        return errors

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'form', 'extras')
        return tpl.generate(element=self)


class CustomField(FormObject):
    """
    """
    type = ContentType('extra.custom')

    def __init__(self, name, **options):
        FormObject.__init__(self, name, **options)

    def validate(self):
        return []

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'form', 'extras')
        return tpl.generate(element=self)