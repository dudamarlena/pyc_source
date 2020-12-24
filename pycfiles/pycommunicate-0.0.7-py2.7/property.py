# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycommunicate\proxies\dom\property.py
# Compiled at: 2016-06-11 13:21:32


class SimpleElementProperty(object):

    def __init__(self, name, element):
        self.name = name
        self.element = element

    def get(self):
        return self.element.dom.controller.socket_interface.request('element.property', self.element.selector, self.name)

    def set(self, value):
        self.element.dom.controller.socket_interface.send('element.property.set', self.element.selector, self.name, value)


class MultiElementProperty(object):

    def __init__(self, basename, element):
        self.element = element
        self.basename = basename