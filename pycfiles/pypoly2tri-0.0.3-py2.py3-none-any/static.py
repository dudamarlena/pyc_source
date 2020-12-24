# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/webpage/form/static.py
# Compiled at: 2011-09-13 05:23:59
import pypoly
from pypoly.content.webpage import ContentType
from pypoly.content.webpage.form import FormObject

class Label(FormObject):
    """
    Use this to create the Label.
    """
    type = ContentType('form.label')

    def __init__(self, name, **options):
        FormObject.__init__(self, name, **options)

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'form', 'static')
        return tpl.generate(element=self)


class LinkLabel(FormObject):
    """
    Use this to create a Link in a form
    """
    url = ''
    type = ContentType('form.label.link')

    def __init__(self, name, **options):
        self.url = ''
        FormObject.__init__(self, name, **options)

    def generate(self):
        tpl = pypoly.template.load_web('webpage', 'form', 'static')
        return tpl.generate(element=self)