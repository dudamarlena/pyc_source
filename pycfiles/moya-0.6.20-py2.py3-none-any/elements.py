# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/elements.py
# Compiled at: 2016-12-08 16:29:22
"""Introspection of Moya elements"""
from __future__ import unicode_literals
from ..elements import Attribute
from ..elements.elementproxy import ElementProxy
from ..tags.context import DataSetter
from .. import errors
from ..logic import DeferNodeContents

class GetParentElement(DataSetter):

    class Help:
        synopis = b'get information about the parent element'

    def get_value(self, context):
        element_proxy = self.parent.get_proxy(context, app=context[b'.app'])
        return element_proxy


class GetElement(DataSetter):
    """Retrieve information regarding an element."""

    class Help:
        synopsis = b'get information about an element'

    name = Attribute(b'Element name')
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', default=None)

    def logic(self, context):
        app = self.get_app(context)
        name = self.name(context)
        dst = self.dst(context)
        element_app, element = self.get_element(name, app=app)
        element_proxy = element.get_proxy(context, element_app)
        self.set_context(context, dst, element_proxy)


class FindElements(DataSetter):
    """Retrieve information regarding elements of a given type."""

    class Help:
        synopsis = b'retrieve information regarding elements of a given type'

    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', type=b'namespace', default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', default=None)

    def logic(self, context):
        ns, tag, dst = self.get_parameters(context, b'ns', b'tag', b'dst')
        app = self.get_app(context)
        if ns is None:
            ns = self.lib.namespace
        let_map = self.get_let_map(context)
        elements = [ ElementProxy(context, None, el) for el in self.archive.get_elements_by_type(ns, tag)
                   ]
        if let_map:
            elements = [ el for el in elements if all(let_map.get(k, None) == el.params.get(k) for k in let_map) ]
        self.set_context(context, dst, elements)
        return


class FindAppElements(DataSetter):
    """
    Retrieve information regarding elements of a given type, with an entry per application.
    """

    class Help:
        synopsis = b'retrieve information regarding elements of a given type'

    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', type=b'namespace', default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', default=None)

    def logic(self, context):
        ns, tag, dst = self.get_parameters(context, b'ns', b'tag', b'dst')
        app = self.get_app(context)
        if ns is None:
            ns = self.lib.namespace
        let_map = self.get_let_map(context)
        archive = self.archive
        elements = []
        for el in archive.get_elements_by_type(ns, tag):
            for app_name in archive.apps_by_lib[el.lib.long_name]:
                app = archive.apps[app_name]
                elements.append(ElementProxy(context, app, el))

        if let_map:
            elements = [ el for el in elements if all(let_map.get(k, None) == el.params.get(k) for k in let_map) ]
        self.set_context(context, dst, elements)
        return


class FindElement(DataSetter):
    """Retrieve an element of a given type."""

    class Help:
        synopsis = b'retrieve information regarding an element'

    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', type=b'namespace', default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', default=None)

    def logic(self, context):
        ns, tag, dst = self.get_parameters(context, b'ns', b'tag', b'dst')
        app = self.get_app(context)
        if ns is None:
            ns = self.lib.namespace
        let_map = self.get_let_map(context)
        for el in self.archive.get_elements_by_type(ns, tag):
            if app and el.lib != app.lib:
                continue
            element = ElementProxy(context, app, el)
            params = element.params
            if all(let_map.get(k, None) == params.get(k) for k in let_map):
                self.set_context(context, dst, element)
                break
        else:
            self.set_context(context, dst, None)

        return


class GetChildren(DataSetter):
    """Get the children of an element."""

    class Help:
        synopsis = b'get an elements children'

    element_ref = Attribute(b'Element Reference', default=None)
    element = Attribute(b'Element', type=b'expression', default=None)
    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', type=b'namespace', default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    data = Attribute(b'Data only', type=b'boolean', default=False)

    def logic(self, context):
        element, element_ref, tag, ns, dst, data = self.get_parameters(context, b'element', b'element_ref', b'tag', b'ns', b'dst', b'data')
        app = getattr(element, b'app', None)
        if element is None and element_ref is None:
            element_ref = self.parent.libid
        if element is not None:
            if not hasattr(element, b'__moyaelement__'):
                self.throw(b'bad-value.not-an-element', (b"Can't get children of '{!r}' because it's not an element").format(element))
            element = element.__moyaelement__()
        elif element_ref is not None:
            try:
                app, element = self.get_element(element_ref)
            except errors.ElementNotFoundError:
                self.throw(b'bad-value.element-not-found', (b"Element with reference '{}' was not found").format(element_ref))

        else:
            self.throw(b'bad-value.missing-element', (b'A valid element is required, not {!r}').format(element))
        if tag:
            if ns is None:
                ns = self.lib.namespace
            children = list(element.children(element_type=(ns, tag)))
        else:
            children = element.get_children()
        children = [ ElementProxy(context, app, el) for el in children ]
        if data:
            children = [ child.params for child in children ]
        self.set_context(context, dst, children)
        return


class ForChildren(DataSetter):
    """Loop for each child of an element"""

    class Help:
        synopsis = b'iterate over the children of an element'

    element_ref = Attribute(b'Element Reference', default=None)
    element = Attribute(b'Element', type=b'expression', default=None)
    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', type=b'namespace')
    dst = Attribute(b'Destination', type=b'reference', default=None)
    data = Attribute(b'Data only', type=b'boolean', default=False)
    filter = Attribute(b'Filter on condition', required=False, type=b'expression', default=True)

    def logic(self, context):
        element, element_ref, tag, ns, dst, data = self.get_parameters(context, b'element', b'element_ref', b'tag', b'ns', b'dst', b'data')
        app = getattr(element, b'app', None)
        if element is not None:
            if not hasattr(element, b'__moyaelement__'):
                self.throw(b'bad-value.not-an-element', (b"Can't get children of '{!r}' because it's not an element").format(element))
            element = element.__moyaelement__()
        else:
            if element_ref is not None:
                try:
                    app, element = self.get_element(element_ref)
                except errors.ElementNotFoundError:
                    self.throw(b'bad-value.not-found', (b"Element with reference '{}' was not found").format(element_ref))

            else:
                self.throw(b'bad-value.missing-element', (b'A valid element is required, not {!r}').format(element))
            if tag:
                if ns is None:
                    ns = self.lib.namespace
                children = list(element.children(element_type=(ns, tag)))
            else:
                children = element.get_children()
            children = [ ElementProxy(context, app, el) for el in children ]
            if data:
                children = [ child.params for child in children ]
            filter = self.filter
            for child in children:
                context[dst] = child
                if filter(context):
                    yield DeferNodeContents(self)

        return


class GetData(DataSetter):
    """Get all data from data tags."""

    class Help:
        synopsis = b'get data from custom data tags'

    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)

    def logic(self, context):
        ns, tag, dst = self.get_parameters(context, b'ns', b'tag', b'dst')
        if ns is None:
            app = self.get_app(context, check=False)
            if app is None:
                self.throw(b'get-data.namespace-missing', b"Couldn't detect namespace (set 'ns' or 'from' attribute)")
            ns = app.lib.namespace
        data = self.archive.get_data(context, ns, tag)
        self.set_context(context, dst, data)
        return


class GetDataItem(DataSetter):
    """Get a single data item."""

    class Help:
        synopsis = b'get data from a single custom tag'

    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', default=None, required=True)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)

    def logic(self, context):
        ns, tag, dst, _from = self.get_parameters(context, b'ns', b'tag', b'dst', b'from')
        lib = None
        app = self.archive.find_app(_from)
        if app is not None:
            lib = app.lib
        data = self.archive.get_data_item(context, ns, tag, self.get_let_map(context), lib=lib)
        self.set_context(context, dst, data)
        return


class GetDataFromElement(DataSetter):
    element = Attribute(b'Element', type=b'expression')
    dst = Attribute(b'Destination', type=b'reference', default=None)

    def logic(self, context):
        element = self.element(context).tag
        data = element.get_all_data_parameters(context)
        self.set_context(context, self.dst(context), data)


class GetDataElements(DataSetter):
    tag = Attribute(b'Element type')
    ns = Attribute(b'XML namespace', default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)
    byapp = Attribute(b'List data elements by app', type=b'boolean', default=False)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)

    def logic(self, context):
        ns, tag, dst, by_app = self.get_parameters(context, b'ns', b'tag', b'dst', b'byapp')
        if ns is None:
            app = self.get_app(context, check=False)
            if app is None:
                self.throw(b'get-data.namespace-missing', b"Couldn't detect namespace (set 'ns' or 'from' attribute)")
            ns = app.lib.namespace
        if by_app:
            data = self.archive.get_app_data_elements(context, ns, tag)
        else:
            data = self.archive.get_data_elements(context, ns, tag)
        self.set_context(context, dst, data)
        return