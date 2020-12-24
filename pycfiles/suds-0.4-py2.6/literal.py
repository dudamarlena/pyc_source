# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/suds/mx/literal.py
# Compiled at: 2010-05-06 19:54:50
"""
Provides literal I{marshaller} classes.
"""
from logging import getLogger
from suds import *
from suds.mx import *
from suds.mx.core import Core
from suds.mx.typer import Typer
from suds.resolver import GraphResolver, Frame
from suds.sax.element import Element
from suds.sudsobject import Factory
log = getLogger(__name__)
Content.extensions.append('type')
Content.extensions.append('real')
Content.extensions.append('ancestry')

class Typed(Core):
    """
    A I{typed} marshaller.
    This marshaller is semi-typed as needed to support both
    I{document/literal} and I{rpc/literal} soap message styles.
    @ivar schema: An xsd schema.
    @type schema: L{xsd.schema.Schema}
    @ivar resolver: A schema type resolver.
    @type resolver: L{GraphResolver}
    """

    def __init__(self, schema, xstq=True):
        """
        @param schema: A schema object
        @type schema: L{xsd.schema.Schema}
        @param xstq: The B{x}ml B{s}chema B{t}ype B{q}ualified flag indicates
            that the I{xsi:type} attribute values should be qualified by namespace.
        @type xstq: bool
        """
        Core.__init__(self)
        self.schema = schema
        self.xstq = xstq
        self.resolver = GraphResolver(self.schema)

    def reset(self):
        self.resolver.reset()

    def start(self, content):
        log.debug('starting content:\n%s', content)
        if content.type is None:
            name = content.tag
            if name.startswith('_'):
                name = '@' + name[1:]
            content.type = self.resolver.find(name, content.value)
            if content.type is None:
                raise TypeNotFound(content.tag)
        else:
            known = None
            if isinstance(content.value, Object):
                known = self.resolver.known(content.value)
                if known is None:
                    log.debug('object has no type information', content.value)
                    known = content.type
            frame = Frame(content.type, resolved=known)
            self.resolver.push(frame)
        frame = self.resolver.top()
        content.real = frame.resolved
        content.ancestry = frame.ancestry
        self.translate(content)
        self.sort(content)
        if self.skip(content):
            log.debug('skipping (optional) content:\n%s', content)
            self.resolver.pop()
            return False
        else:
            return True
            return

    def suspend(self, content):
        self.resolver.pop()

    def resume(self, content):
        self.resolver.push(Frame(content.type))

    def end(self, parent, content):
        log.debug('ending content:\n%s', content)
        current = self.resolver.top().type
        if current == content.type:
            self.resolver.pop()
        else:
            raise Exception, 'content (end) mismatch: top=(%s) cont=(%s)' % (
             current, content)

    def node(self, content):
        ns = content.type.namespace()
        if content.type.form_qualified:
            node = Element(content.tag, ns=ns)
            node.addPrefix(ns[0], ns[1])
        else:
            node = Element(content.tag)
        self.encode(node, content)
        log.debug('created - node:\n%s', node)
        return node

    def setnil(self, node, content):
        if content.type.nillable:
            node.setnil()

    def setdefault(self, node, content):
        default = content.type.default
        if default is None:
            pass
        else:
            node.setText(default)
        return default

    def optional(self, content):
        if content.type.optional():
            return True
        for a in content.ancestry:
            if a.optional():
                return True

        return False

    def encode(self, node, content):
        if content.type.any():
            return
        else:
            if not content.real.extension():
                return
            if content.type.resolve() == content.real:
                return
            ns = None
            name = content.real.name
            if self.xstq:
                ns = content.real.namespace('ns1')
            Typer.manual(node, name, ns)
            return

    def skip(self, content):
        """
        Get whether to skip this I{content}.
        Should be skipped when the content is optional
        and either the value=None or the value is an empty list.
        @param content: The content to skip.
        @type content: L{Object}
        @return: True if content is to be skipped.
        @rtype: bool
        """
        if self.optional(content):
            v = content.value
            if v is None:
                return True
            if isinstance(v, (list, tuple)) and len(v) == 0:
                return True
        return False

    def optional(self, content):
        if content.type.optional():
            return True
        for a in content.ancestry:
            if a.optional():
                return True

        return False

    def translate(self, content):
        """
        Translate using the XSD type information.
        Python I{dict} is translated to a suds object.  Most
        importantly, primative values are translated from python
        types to XML types using the XSD type.
        @param content: The content to translate.
        @type content: L{Object}
        @return: self
        @rtype: L{Typed}
        """
        v = content.value
        if v is None:
            return
        else:
            if isinstance(v, dict):
                cls = content.real.name
                content.value = Factory.object(cls, v)
                md = content.value.__metadata__
                md.sxtype = content.type
                return
            v = content.real.translate(v, False)
            content.value = v
            return self

    def sort(self, content):
        """
        Sort suds object attributes based on ordering defined
        in the XSD type information.
        @param content: The content to sort.
        @type content: L{Object}
        @return: self
        @rtype: L{Typed}
        """
        v = content.value
        if isinstance(v, Object):
            md = v.__metadata__
            md.ordering = self.ordering(content.real)
        return self

    def ordering(self, type):
        """
        Get the attribute ordering defined in the specified
        XSD type information.
        @param type: An XSD type object.
        @type type: SchemaObject
        @return: An ordered list of attribute names.
        @rtype: list
        """
        result = []
        for (child, ancestry) in type.resolve():
            name = child.name
            if child.name is None:
                continue
            if child.isattr():
                name = '_%s' % child.name
            result.append(name)

        return result


class Literal(Typed):
    """
    A I{literal} marshaller.
    This marshaller is semi-typed as needed to support both
    I{document/literal} and I{rpc/literal} soap message styles.
    """
    pass