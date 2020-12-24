# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/webpage/form/text.py
# Compiled at: 2011-09-13 07:35:39
import pypoly
from pypoly.content.webpage import CSS, ContentType
from pypoly.content.webpage.form import FormObject

class Textarea(FormObject):
    """
    """
    type = ContentType('form.text.area')

    def __init__(self, name, **options):
        FormObject.__init__(self, name, **options)
        self._type = 'textarea'

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.raw_value = str(value)

    value = property(_get_value, _set_value)

    def validate(self):
        errors = []
        self._value = self.raw_value
        errors = errors + FormObject.validate(self)
        if len(errors) > 0:
            self._value = None
        return errors

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'form', 'textarea')
        return tpl.generate(element=self)


class WYSIWYG(FormObject):
    """
    """
    type = ContentType('form.text.wysiwyg')

    def __init__(self, name, **options):
        FormObject.__init__(self, name, **options)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.raw_value = str(value)

    value = property(_get_value, _set_value)

    def validate(self):
        errors = []
        self._value = self.raw_value
        errors = errors + FormObject.validate(self)
        if len(errors) > 0:
            self._value = None
        return errors

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'form', 'wysiwyg')
        return tpl.generate(element=self)