# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/elements/elementproxy.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from ..interface import AttributeExposer
import weakref

class ElementProxy(AttributeExposer):
    __moya_exposed_attributes__ = [
     b'app',
     b'tag',
     b'params',
     b'attributes',
     b'element_ref',
     b'tag_name',
     b'tag_xmlns',
     b'tag_type',
     b'parent']

    def __init__(self, context, app, element):
        self._context = weakref.ref(context)
        self.app = app
        self.tag = element
        self.attributes = element.get_all_parameters(context)
        self.element_ref = (b'{}#{}').format(app.name if app else element.lib.long_name, element.libname)
        self.tag_name = element._tag_name
        self.tag_xmlns = element.xmlns
        self.tag_type = (b'{{{}}}{}').format(self.tag_xmlns, self.tag_name)

    @property
    def context(self):
        return self._context()

    @property
    def params(self):
        return self.attributes

    @property
    def parent(self):
        if not self.tag.parent:
            return None
        else:
            return ElementProxy(self.context, self.app, self.tag.parent)

    def __moyaelement__(self):
        return self.tag

    def __repr__(self):
        return (b'<element {}>').format(self.element_ref)

    def __moyaconsole__(self, context, console):
        obj_params = dict(app=self.app, tag_name=self.tag_name, tag=self.tag, atributes=self.attributes, element_ref=self.element_ref)
        console.obj(context, obj_params)

    def qualify(self, app):
        self.app = app
        self.element_ref = (b'{}#{}').format(app.name if app else element.lib.long_name, element.libname)


class DataElementProxy(AttributeExposer):
    __moya_exposed_attributes__ = [
     b'app',
     b'tag',
     b'params',
     b'attributes',
     b'element_ref',
     b'tag_name',
     b'tag_xmlns',
     b'tag_type',
     b'data',
     b'parent']

    def __init__(self, context, app, element, data):
        self.app = app
        self.tag = element
        self.attributes = element.get_all_parameters(context)
        self.element_ref = (b'{}#{}').format(app.name if app else element.lib.long_name, element.libname)
        self.tag_name = element._tag_name
        self.data = data
        self.tag_xmlns = element.xmlns
        self.tag_type = (b'{{{}}}{}').format(self.tag_xmlns, self.tag_name)

    @property
    def params(self):
        return self.attributes

    def __moyaelement__(self):
        return self.tag

    def __repr__(self):
        return (b'<element {}>').format(self.element_ref)

    def __moyaconsole__(self, context, console):
        obj_params = dict(app=self.app, tag_name=self.tag_name, tag=self.tag, attributes=self.attributes, element_ref=self.element_ref, data=self.data)
        console.obj(context, obj_params)