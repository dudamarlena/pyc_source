# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/html.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..elements.registry import ElementRegistry
from ..elements.elementbase import LogicElement, DynamicElementMixin
from ..template.moyatemplates import Template
from ..html import escape
from ..render import HTML
from .. import logic
from .. import namespaces

def make_html_tag(_tag_name):

    class DynamicHTMLTag(LogicElement, DynamicElementMixin):
        xmlns = namespaces.html
        template = Template(b'<${tag_name}${tag_attribs}>{% children %}</${tag_name}>', __file__)

        class Meta:
            text_nodes = b'text'
            dynamic = True
            tag_name = _tag_name
            translate = False
            all_attributes = True

        def logic(self, context):
            sub = context.sub
            tag_attribs = b' ' + (b' ').join((b'{}="{}"').format(escape(k), escape(sub(v))) for k, v in self._attrs.items() if k != b'if')
            td = {b'tag_attribs': HTML(tag_attribs.rstrip()), b'tag_name': HTML(_tag_name)}
            content = context[b'.content']
            content.add_template(self._tag_name, self.template, td)
            with content.node():
                yield logic.DeferNodeContents(self)

    return DynamicHTMLTag


ElementRegistry.default_registry.add_dynamic_registry(namespaces.html, make_html_tag)