# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/ploneformgen/readonlystringfield/widget.py
# Compiled at: 2009-03-24 10:52:05
from Products.Archetypes.Widget import StringWidget
from Products.Archetypes.Registry import registerWidget

class ReadonlyStringWidget(StringWidget):
    __module__ = __name__
    _properties = StringWidget._properties.copy()
    _properties.update({'macro': 'readonlystring'})


registerWidget(ReadonlyStringWidget, title='ReadonlyString', description='Renders a HTML readonly text input box which accepts a single line of text', used_for=('Products.Archetypes.Field.StringField', ))