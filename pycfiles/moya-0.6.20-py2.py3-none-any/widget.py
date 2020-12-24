# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/widget.py
# Compiled at: 2015-11-07 06:12:06
from __future__ import unicode_literals
from __future__ import print_function
from ..elements.registry import Meta
from ..elements import attributetypes
from ..elements.elementbase import ElementBase, Attribute, LogicElement
from ..logic import DeferNodeContents
from ..tools import textual_list, nearest_word
from ..context.missing import is_missing
from ..context.tools import to_expression
from ..compat import text_type, py2bytes
from .. import errors
from .. import namespaces
from collections import OrderedDict

class WidgetBase(LogicElement):
    _container = False

    class Meta:
        text_nodes = b'text'
        is_call = True

    class NoTextMeta:
        text_nodes = None
        is_call = True

    def __init__(self, *args, **kwargs):
        self.init_args = (
         args, kwargs)
        super(WidgetBase, self).__init__(*args, **kwargs)

    def get_widget_app(self, context):
        app = None
        if self.has_parameter(b'from'):
            app = self.get_parameter(context, b'from') or None
        if app is None:
            try:
                app = self.archive.detect_app(context, self._lib_long_name)
            except:
                app = None

        if app is None:
            self.throw(b'widget.ambiguous-app', b"unable to detect app for this widget (you may need to supply the 'from' attribute)")
        return app

    def logic(self, context):
        widget_frame = context.current_frame
        content = context[b'.content']
        if is_missing(content):
            self.throw(b'widget.content-missing', b'widgets must be called in a content definition')
        td = self.get_all_parameters(context)
        td.pop(b'_if', None)
        _cachekey, _cachefor = self._cache
        cachekey, cachefor = (None, None)
        let_map = self.get_let_map(context)
        widget_app = self.get_widget_app(context)
        if _cachekey and _cachefor:
            with context.data_frame(td):
                cachekey = _cachekey(context)
                cachefor = _cachefor(context).milliseconds
            cachekey = (b'__widget__.{}.{}').format(self.libid, cachekey)
            cache = self.archive.get_cache(b'fragment')
            html = cache.get(cachekey, None)
            if html is not None:
                content.add_markup(self._tag_name, html)
                return
        if b'_caller' not in td:
            td[b'_caller'] = self.get_proxy(context, context[b'.app'])

        def on_yield(context, app, content, element, data):
            context.push_frame(widget_frame)
            try:
                with self.defer(context, app=app):
                    with context.data_scope(data):
                        with content.node():
                            yield DeferNodeContents(element)
            finally:
                context.pop_frame()

        app = self.get_app(context)
        self.push_call(context, td, widget_app)
        if self._let_dst:
            context[self._let_dst] = let_map
        if self.has_parameter(b'template'):
            template = app.resolve_templates(self.template(context), check=True)
        else:
            template = widget_app.resolve_templates(self._template(context), check=True)
        template_node = content.add_template(self._tag_name, template, app=widget_app)
        yield_stack = context.set_new_call(b'._yield_stack', list)
        yield_stack.append(lambda c, data: on_yield(c, app, content, self, data))
        try:
            if self.widget_element.has_children:
                yield DeferNodeContents(self.widget_element)
        finally:
            yield_stack.pop()
            scope = context.obj
            self.pop_call(context)

        if self._container and self.has_children:
            with content.node():
                yield DeferNodeContents(self)
        if b'_return' in scope:
            scope = scope[b'_return']
            if hasattr(scope, b'get_return_value'):
                scope = scope.get_return_value()
            if not scope:
                scope = {}
            if not hasattr(scope, b'items'):
                self.throw(b'widget.return-no-dict', (b'the return value from a widget must be a dict, or None (not {})').format(context.to_expr(scope)))
        template_node.update_template_data(scope)
        if cachekey is not None:
            html = template_node.moya_render(self.archive, context, b'html', {})
            cache = self.archive.get_cache(b'fragment')
            cache.set(cachekey, html, cachefor)
        return


class WidgetBaseContainer(WidgetBase):
    _container = True


class WidgetYield(LogicElement):
    """Yield to a widget block"""

    class Help:
        synopsis = b'yield to code block in a widget'

    obj = Attribute(b'Data to yield', type=b'expression', required=False, default=None)

    def logic(self, context):
        yield_call = context.get_stack_top(b'yield')
        yield_data = self.obj(context) or {}
        yield_data.update(self.get_let_map(context))
        if callable(yield_call):
            for node in yield_call(context, yield_data.copy()):
                yield node


class Widget(ElementBase):
    """Create a widget"""

    class Help:
        synopsis = b'create a re-uasable widget'

    ns = Attribute(b'XML Namespace', required=False)
    name = Attribute(b'Tag name', required=True)
    template = Attribute(b'Template', type=b'templates', required=False, default=None)
    let = Attribute(b'Let destination', required=False, default=None)
    container = Attribute(b'Is this widget a container?', type=b'boolean', default=True, required=False)
    synopsis = Attribute(b'Short description of the widget')
    undocumented = Attribute(b'Set to yes to disabled documentation for this tag', type=b'boolean', default=False)
    text = Attribute(b'Include text children?', type=b'boolean', default=True)
    cachekey = Attribute(b'Cache key', name=b'cachekey', type=b'text', default=None, required=False)
    cachefor = Attribute(b'Cache time', name=b'cachefor', type=b'timespan', default=None, required=False)

    def finalize(self, context):
        params = self.get_parameters(context)
        attributes = {}
        attributes[b'template'] = Attribute(b'Override widget template', name=b'template', type=b'templates', required=False, default=None)
        for signature in self.children(b'signature'):
            for attribute_tag in signature.children(b'attribute'):
                param_map = attribute_tag.get_all_parameters(context)
                if attribute_tag.has_parameter(b'default') and not attribute_tag.has_parameter(b'required'):
                    param_map[b'required'] = False
                description = attribute_tag.doc
                name = param_map.pop(b'name')
                attribute = Attribute(description, name=name, evaldefault=True, **param_map)
                attributes[attribute.name] = attribute

        attributes[b'from'] = Attribute(b'Application', name=b'from', type=b'application', map_to=b'from', default=None)
        doc = None
        for doc_tag in self.children(b'doc'):
            doc = doc_tag.text.strip()

        meta = Meta()
        meta.is_call = True

        class Help(object):
            synopsis = params.synopsis
            undocumented = params.undocumented

        cls_dict = dict(__doc__=text_type(doc or b''), Meta=meta, Help=Help)
        if self.source_line:
            definition = b'%s (line %s)' % (self._location, self.source_line)
        else:
            definition = self._location
        cls_dict[b'_definition'] = definition
        cls_dict[b'_template'] = self.template
        cls_dict[b'_let_dst'] = params.let
        if self.has_parameters(b'cachekey', b'cachefor'):
            cls_dict[b'_cache'] = (
             self.cachekey, self.cachefor)
        else:
            cls_dict[b'_cache'] = (None, None)
        cls_dict[b'xmlns'] = params.ns or self.lib.namespace or namespaces.default
        cls_dict.update((b'_attribute_' + k, v) for k, v in attributes.items())
        if params.text:
            cls_dict[b'Meta'] = WidgetBase.Meta
        else:
            cls_dict[b'Meta'] = WidgetBase.NoTextMeta
        cls_dict[b'_registry'] = self.archive.registry
        if params.container:
            bases = (
             WidgetBaseContainer,)
        else:
            bases = (
             WidgetBase,)
        tag_class = type(py2bytes(params.name), bases, cls_dict)
        tag_class.widget_element = self
        tag_class.libname = None
        tag_class._definition = definition
        tag_class._lib_long_name = context.get(b'._lib_long_name', None)
        return


class AttributeTag(ElementBase):
    """Defines an attribute in a [tag]tag[/tag], [tag]data-tag[/tag] or [tag]widget[/tag]."""

    class Help:
        synopsis = b'define an attribute in a custom tag'
        example = b'\n        <datatag name="module">\n            <doc>Define a top level admin module</doc>\n            <signature>\n                <attribute name="slug" required="yes" />\n                <attribute name="title" required="yes" />\n                <attribute name="description" required="yes" />\n                <attribute name="content" type="elementref" required="no" />\n            </signature>\n        </datatag>\n\n        '

    _element_class = b'widget'
    preserve_attributes = [b'doc']

    class Meta:
        logic_skip = True
        tag_name = b'attribute'

    name = Attribute(b'Name of the attribute', required=True)
    type = Attribute(b'Type of the attribute', required=False, default=b'expression', choices=attributetypes.valid_types)
    required = Attribute(b'Required', type=b'boolean', required=False, default=True)
    default = Attribute(b'Default', required=False, default=None)
    metavar = Attribute(b'Metavar (identifier used in documentation)', required=False)
    missing = Attribute(b'Are missing values allowed?', type=b'boolean', default=True, required=False)
    empty = Attribute(b'Are empty values allowed?', type=b'boolean', default=True, required=False)
    choices = Attribute(b'Valid values for this attribute', type=b'commalist', default=None, required=False)

    def post_build(self, context):
        self.doc = context.sub(self.text.strip())


class ArgumentTag(ElementBase):
    """
    Defines an argument to a macro.

    The text of this tag should document the purpose of the argument.

    """

    class Help:
        synopsis = b'define an argument to a macro'
        example = b'\n        <macro docname="average">\n            <signature>\n                <argument name="numbers" required="yes" check="len:numbers gt 0">\n                    A list (or other sequence) of numbers\n                </argument>\n            </signature>\n            <return value="sum:numbers / len:numbers" />\n        </macro>\n\n        '

    class Meta:
        logic_skip = True
        tag_name = b'argument'

    name = Attribute(b'Name of the attribute', required=True)
    required = Attribute(b'Is this argument required?', type=b'boolean', default=True)
    check = Attribute(b'A boolean expression that the attribute must satisfy', type=b'function', default=None)
    default = Attribute(b'A value to use if the argument is not supplied', type=b'function', default=None)

    def post_build(self, context):
        self.doc = context.sub(self.text.strip())


class ArgumentValidator(object):
    """Checks arguments to a macro call."""

    def __init__(self, context, element):
        self.doc = []
        self.required = []
        self.checks = []
        self.arg_names = set()
        self.defaults = OrderedDict()
        for arg in element.children():
            if arg._element_type != (namespaces.default, b'argument'):
                raise errors.ElementError((b'{} signature must contain <argument> tags only').format(element.parent), element=element)
            name, required, check, default = arg.get_parameters(context, b'name', b'required', b'check', b'default')
            if arg.has_parameter(b'default'):
                self.defaults[name] = default
                required = False
            self.arg_names.add(name)
            if required:
                self.required.append(name)
            if check is not None:
                self.checks.append((name, check))
            self.doc.append({b'name': name, b'required': required, b'check': check})

        self.required_set = frozenset(self.required)
        return

    def __repr__(self):
        if self.arg_names:
            return (b'<validator {}>').format(textual_list(self.arg_names))
        else:
            return b'<validator>'

    def check(self, context, arg_map, checked_object):
        for k, default in self.defaults.items():
            if k not in arg_map:
                arg_map[k] = default(context)

        if not self.arg_names.issuperset(arg_map.keys()):
            for k in self.arg_names:
                if k not in arg_map:
                    raise ValueError((b"'{}' is a required argument to {}").format(k, checked_object))

        for name, check in self.checks:
            try:
                result = check.call(context, arg_map)
            except Exception as e:
                raise ValueError((b"check failed for argument '{}' with error '{}'").format(name, e))

            if not result:
                raise ValueError((b'{value} is not a valid value for argument {name}').format(name=name, value=to_expression(context, arg_map[name])))

    def validate(self, context, element, arg_map):
        for k, default in self.defaults.items():
            if k not in arg_map:
                arg_map[k] = default(context)

        if not self.arg_names.issuperset(arg_map.keys()):
            for k in arg_map:
                if k not in self.arg_names:
                    nearest = nearest_word(k, self.arg_names)
                    if nearest is not None:
                        diagnosis = (b"Did you mean '{}'?").format(nearest)
                    else:
                        diagnosis = (b'Valid arguments to this macro are {}.').format(textual_list(sorted(self.arg_names), b'and'))
                    element.throw(b'argument-error.unknown-argument', (b"no argument called '{name}' in {element}'").format(name=k, element=element), diagnosis=diagnosis)

        if not self.required_set.issubset(arg_map.keys()):
            for name in self.required:
                if name not in arg_map:
                    element.throw(b'argument-error.required', (b"argument '{}' is required in {}").format(name, element), diagnosis=(b'You can pass a value for \'{name}\' with let:{name}="<VALUE>" ').format(name=name, element=element))

        for name, check in self.checks:
            try:
                result = check.call(context, arg_map)
            except Exception as e:
                element.throw(b'argument-error.check-error', (b"check for argument '{}' in {} failed with exception: {}").format(name, element, e), diagnosis=(b"An exception was thrown when evaluating the expression '{}'.\n\nThis could indicate a programming error in the macro or Moya.").format(check.expression))

            if not result:
                diagnosis_msg = b"{value} is not a valid value for argument '{name}'. Check the calling logic is correct."
                element.throw(b'argument-error.check-failed', (b'argument \'{}\' failed check "{}" in {}').format(name, check.expression, element), diagnosis=diagnosis_msg.format(name=name, value=to_expression(context, arg_map[name]), element=element))

        return


class Signature(ElementBase):
    """
    Begins a list of attributes and arguments for a [tag]tag[/tag], [tag]data-tag[/tag], [tag]macro[/tag] or [tag]command[/tag].

    In the case of tags, the signature should contain [tag]attribute[/tag] tags.
    Macros expect [tag]argument[/tag] tags.
    For a command, the signature should contain [tag]arg[/tag] and [tag]option[/tag] tags.

    """
    _element_class = b'widget'

    class Help:
        synopsis = b'define the attributes / arguments to a tag / macro'
        example = b'\n        <tag name="fib">\n            <doc>Calculate the fibonacci sequence</doc>\n            <signature>\n                <attribute name="count" type="integer" />\n            </signature>\n            <let fib="[0, 1]"/>\n            <repeat times="count - 2">\n                <append value="fib[-1] + fib[-2]" dst="fib" />\n            </repeat>\n            <return value="fib" />\n        </tag>\n\n        '

    class Meta:
        logic_skip = True

    def get_validator(self, context):
        return ArgumentValidator(context, self)

    def finalize(self, context):
        if self.parent._element_type in ((namespaces.default, b'macro'), (namespaces.default, b'Filter')):
            self.validator = ArgumentValidator(context, self)
        else:
            self.validator = None
        return


class Doc(ElementBase):
    """
    Write documentation for a widget or custom tag.

    """
    _element_class = b'doc'

    class Meta:
        logic_skip = True

    class Help:
        synopsis = b'document a tag'
        example = b'\n        <widget name="post" template="post.html">\n            <doc>Renders a single post</doc>\n            <!-- widget code -->\n        </widget>\n\n        '