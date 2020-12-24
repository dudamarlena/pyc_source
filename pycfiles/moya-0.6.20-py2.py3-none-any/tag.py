# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/tag.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..elements.registry import Meta
from ..elements.elementbase import ElementBase, Attribute, LogicElement, MoyaAttributeError
from ..elements.elementproxy import DataElementProxy
from ..logic import DeferNodeContents
from ..tags.context import _LazyCallable, DataSetter
from ..context.missing import is_missing
from ..compat import text_type, py2bytes
from .. import errors

class TagBase(LogicElement):

    def __init__(self, *args, **kwargs):
        self.init_args = (
         args, kwargs)
        super(TagBase, self).__init__(*args, **kwargs)

    def get_tag_app(self, context):
        app = None
        if self.has_parameter(b'from'):
            app = self.get_parameter(context, b'from') or None
        if app is None:
            try:
                app = self.archive.get_app_from_lib(self._lib_long_name, current=context[b'.app'])
            except Exception as e:
                if app is None:
                    self.throw(b'tag.ambiguous-app', text_type(e), diagnosis=b"You may need to supply the 'from' attribute")

        return app

    def logic(self, context):
        dst, lazy = self.get_parameters(context, b'dst', b'lazy')
        params = self.get_all_parameters(context)
        if self._let_dst:
            params[self._let_dst] = self.get_let_map(context)
        if b'_caller' not in params:
            params[b'_caller'] = self.get_proxy(context, context[b'.app'])
        app = self.get_tag_app(context)
        if lazy and dst:
            element_callable = self.archive.get_callable_from_element(self.element, app=app)
            lazy_callable = _LazyCallable(context, element_callable, (), params)
            context.set_lazy(dst, lazy_callable)
        else:
            macro_call = self.push_call(context, {}, app=app, yield_element=self, yield_frame=context.current_frame)
            try:
                macro_call.update(params)
                yield DeferNodeContents(self.element)
            finally:
                call = self.pop_call(context)
                if b'_return' in call:
                    value = _return = call[b'_return']
                    if hasattr(_return, b'get_return_value'):
                        value = _return.get_return_value()
                else:
                    value = None
                if dst is None:
                    getattr(context.obj, b'append', lambda a: None)(value)
                else:
                    context[dst] = value

        return


class Yield(LogicElement):
    """Yield from a tag"""

    class Help:
        synopsis = b'yield to code block'

    scope = Attribute(b'scope to use', type=b'expression', default=None)

    def logic(self, context):
        scope = self.scope(context)
        if scope is None:
            scope = {}
        scope.update(self.get_let_map(context))
        call = context[b'.call']
        if is_missing(call) or not call.yield_frame:
            self.throw(b'yield.cant-yield', b"Can't yield from here")
        if scope:
            context.push_frame(call.yield_frame)
            try:
                with context.data_scope(scope):
                    yield DeferNodeContents(call.yield_element)
            finally:
                context.pop_frame()

        else:
            context.push_frame(call.yield_frame)
            try:
                yield DeferNodeContents(call.yield_element)
            finally:
                context.pop_frame()

        return


class GetTagText(DataSetter):
    """
    Get the XML text associated with the parent tag.

    """

    class Help:
        synopsis = b'get text from the parent tag'

    sub = Attribute(b'Substitute the text?', type=b'boolean', default=False)
    strip = Attribute(b'Strip text?', type=b'boolean', default=True)

    def get_value(self, context):
        call = context[b'.call']
        try:
            element = call.yield_element
        except AttributeError:
            self.throw(b'get-tag-text.error', b'Unable to retrieve tag text here')

        if element is None:
            self.throw(b'get-tag-text.error', b'Unable to detect parent tag')
        text = element.text
        if self.sub(context):
            context.push_frame(call.yield_frame)
            try:
                text = context.sub(text)
            finally:
                context.pop_frame()

        if self.strip(context):
            text = text.strip()
        return text


class Tag(ElementBase):
    """
    Define a custom tag. A custom tag is in a callable tag that works like builtin logic tags. Here's an example of defining a custom tag:

    [code xml]
    <tag name="getstock">
        <doc>Get count of available stock</doc>
        <signature>
            <attribute name="product" />
        </signature>
        <db:get model="#Product.name == product" dst="product"/>
        <return value="product.count"/>
    </tag>
    [/code]

    You may define a custom tag anywhere in a library. Once defined, the tag is available to any code that uses the appropriate namespace defined in [c]lib.ini[/c]. For example, if the above tag is defined in a library with an xml namespace of [c]http://moyaproject.com/sushifinder[/c], it could be invoked with the following file:

    [code xml]
    <moya xmlns:sushifinder="http://moyaproject.com/sushifinder">
        <macro name="main">
            <sushifinder:getstock product="tuna-roll" dst="count" />
            <echo>We have ${count} tuna rolls in stock.</echo>
        </macro>
    </moya>
    [/code]

    Custom tags are preferred over macros when exposing functionality to other libraries.

    """

    class Help:
        synopsis = b'define a custom tag'

    ns = Attribute(b'XML Namespace', required=False, default=None)
    name = Attribute(b'Tag name', required=True)
    synopsis = Attribute(b'Short description of tag')
    undocumented = Attribute(b'Set to yes to disabled documentation for this tag', type=b'boolean', default=False)
    let = Attribute(b'Let destination', required=False, default=None)
    _tag_base = TagBase

    def finalize(self, context):
        params = self.get_parameters(context)
        attributes = {}
        try:
            for signature in self.children(b'signature'):
                for attribute_tag in signature.children(b'attribute'):
                    param_map = attribute_tag.get_all_parameters(context)
                    if attribute_tag.has_parameter(b'default') and not attribute_tag.has_parameter(b'required'):
                        param_map[b'required'] = False
                    attribute = Attribute(attribute_tag.doc, map_to=param_map.get(b'name'), evaldefault=True, **param_map)
                    attributes[attribute.name] = attribute

        except MoyaAttributeError as e:
            raise errors.ElementError(text_type(e), element=self)

        if b'dst' not in attributes:
            attributes[b'dst'] = Attribute(b'Destination', name=b'dst', type=b'reference', map_to=b'dst', default=None)
        if b'lazy' not in attributes:
            attributes[b'lazy'] = Attribute(b'Enable lazy evaluation', name=b'lazy', type=b'boolean', map_to=b'lazy', default=False)
        attributes[b'from'] = Attribute(b'Application', name=b'from', type=b'application', map_to=b'from', default=None)
        doc = None
        for doc_tag in self.children(b'doc'):
            doc = doc_tag.text.strip()

        meta = Meta()
        meta.is_call = True
        cls_dict = dict(__doc__=text_type(doc or b''), Meta=meta)
        if self.source_line:
            definition = b'%s (line %s)' % (self._location, self.source_line)
        else:
            definition = self._location

        class Help(object):
            synopsis = params.synopsis
            undocumented = params.undocumented

        ns = params.ns or self.lib.namespace
        if not ns:
            _msg = b'could not detect namespace for custom tag "{}" -- please specify the namespace with the "ns" attribute or in lib.ini'
            raise errors.ElementError(_msg.format(params.name), element=self)
        cls_dict.update({b'Help': Help, b'xmlns': ns, 
           b'_registry': self.archive.registry, 
           b'element': self, 
           b'libname': None, 
           b'_definition': definition, 
           b'_location': self._location, 
           b'source_line': self.source_line, 
           b'_code': self._code, 
           b'_lib_long_name': context.get(b'._lib_long_name', None)})
        cls_dict[b'_let_dst'] = params.let
        cls_dict.update({b'_attribute_' + k:v for k, v in attributes.items()})
        tag_class = type(py2bytes(params.name), (
         self._tag_base,), cls_dict)
        tag_class._definition = definition
        return


class DataTagBase(LogicElement):

    def __init__(self, *args, **kwargs):
        self.init_args = (
         args, kwargs)
        super(DataTagBase, self).__init__(*args, **kwargs)

    def get_proxy(self, context, app):
        return DataElementProxy(context, app, self, self.get_all_data_parameters(context))

    def finalize(self, context):
        self.archive.add_data_tag(self._element_type, self)


class DataTag(ElementBase):
    """Define a data tag. See [doc customtags]."""
    ns = Attribute(b'XML Namespace', required=False, default=None)
    name = Attribute(b'Tag name', required=True)
    synopsis = Attribute(b'Short description of the data tag')
    undocumented = Attribute(b'Set to yes to disabled documentation for this tag', type=b'boolean', default=False)
    _tag_base = DataTagBase

    class Help:
        synopsis = b'define a data tag'

    def finalize(self, context):
        params = self.get_parameters(context)
        attributes = {}
        for signature in self.children(b'signature'):
            for attribute_tag in signature.children(b'attribute'):
                param_map = attribute_tag.get_all_parameters(context)
                if attribute_tag.has_parameter(b'default') and not attribute_tag.has_parameter(b'required'):
                    param_map[b'required'] = False
                attribute = Attribute(attribute_tag.doc, map_to=param_map.get(b'name'), evaldefault=True, **param_map)
                attributes[attribute.name] = attribute

        doc = None
        for doc_tag in self.children(b'doc'):
            doc = doc_tag.text.strip()

        meta = Meta()
        meta.logic_skip = True
        meta.is_call = False

        class Help(object):
            synopsis = params.synopsis
            undocumented = params.undocumented

        cls_dict = dict(__doc__=text_type(doc or b''), Meta=meta, Help=Help)
        if self.source_line:
            definition = b'%s (line %s)' % (self._location, self.source_line)
        else:
            definition = self._location
        cls_dict[b'_definition'] = definition
        cls_dict[b'xmlns'] = params.ns or self.lib.namespace
        cls_dict.update({b'_attribute_' + k:v for k, v in attributes.items()})
        cls_dict[b'_registry'] = self.archive.registry
        tag_class = type(py2bytes(params.name), (
         self._tag_base,), cls_dict)
        tag_class.element = self
        tag_class._definition = definition
        return