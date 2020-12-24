# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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