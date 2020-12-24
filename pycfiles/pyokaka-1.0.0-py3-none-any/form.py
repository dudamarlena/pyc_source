# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dijit\form.py
# Compiled at: 2013-06-05 12:09:39
from pyojo.js.code import Code
from pyojo.js.dojo._base import Dojo
from . import Dijit

class Button(Dijit):
    """ 
        @param label: Label
        @param onClick: function
    
    """
    startup = False
    require = ['dojo/ready', 'dijit/form/Button']


class SimpleTextarea(Dojo):
    require = [
     'dojo/ready', 'dijit/form/SimpleTextarea']

    def __init__(self, name, target):
        self.loc = "var %s = new SimpleTextarea({rows:4}, '%s');" % (name,
         target)


sss = '[      { label: "Español", value: "ES", selected: true },\n                { label: "Inglés", value: "EN" },\n                { label: "Alemán", value: "GR" },\n                { label: "Francés", value: "FR" },\n                { label: "Chino", value: "CH" }\n      ]'

class Select(Dijit):
    require = [
     'dojo/ready', 'dijit/form/Select']

    def init(self):
        self.para.update({'name': self.name, 'options': Code(sss)})