# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\examples\base_template.py
# Compiled at: 2017-03-24 11:59:47
from evgen.core import BaseTemplate
from random import choice

class External:

    def __init__(self):
        self.Dupa = 'dupa'


class MyTemplate(BaseTemplate):

    def __init__(self):
        BaseTemplate.__init__(self)
        self.External = None
        self.PrivateProp = 'abc'
        self.set_attribute('static', 1)
        self.set_attribute('dynamic', self.generate_dynamic_prop)
        self.set_attribute('external', self.get_external_val)
        return

    def add_external(self, ext):
        self.External = ext

    def get_external_val(self):
        return self.External.Dupa

    def generate_dynamic_prop(self):
        random_vals = range(5)
        return choice(random_vals)

    def basic_func(self):
        return 'basic func'


mt = MyTemplate()
print mt.static
print mt.dynamic
print mt.Attributes
print mt.Attributes.get('static')
mt.update_attributes({'a': 'b'})
print mt.Attributes
print mt.PrivateProp
print mt.basic_func()
mt.add_external(External())
print mt.external