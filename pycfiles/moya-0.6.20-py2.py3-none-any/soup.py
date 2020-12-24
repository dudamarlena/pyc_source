# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/soup.py
# Compiled at: 2017-07-13 14:54:39
from __future__ import unicode_literals
from __future__ import print_function
from ..elements.elementbase import Attribute
from ..tags.context import DataSetter
from ..compat import text_type
from ..html import slugify
from .. import namespaces
from lxml.cssselect import CSSSelector
from lxml.html import tostring, fromstring, fragment_fromstring
import json

class HTMLTag(object):
    """Represents an HTML tag."""

    def __init__(self, el):
        self._el = el
        self.name = el.tag
        self.attribs = dict(el.items())
        self.text = el.text

    def __repr__(self):
        return tostring(self._el).decode(b'utf-8').strip()


class Strain(DataSetter):
    """
    Manipulate HTML with CSS selectors.

    The [c]select[/c] attribute should be a CSS selector which will filter tags from the [c]src[/c] string. The other attributes define what should happen to the matches tags.

    The following example defines a [tag]filter[/tag] which uses [tag]{soup}strain[/tag] to add [c]class="lead"[/c] to the first paragraph of HTML:

    [code xml]
    <filter name="leadp" value="html">
        <doc>Add class="lead" to first paragraph</doc>
        <soup:strain src="html" select="p" max="1" let:class="'lead'" dst="leadp"/>
        <return value="html:leadp"/>
    </filter>
    [/code]

    """
    xmlns = namespaces.soup

    class Help:
        synopsis = b'modify HTML with CSS selectors'

    select = Attribute(b'CSS selector', type=b'text', default=b'*')
    src = Attribute(b'HTML document or fragment', type=b'expression', required=True)
    append = Attribute(b'markup to append', type=b'expression', required=False, default=None)
    prepend = Attribute(b'markup to prepend', type=b'expression', required=False, default=None)
    replace = Attribute(b'markup to replace', type=b'expression', required=False, default=None)
    remove = Attribute(b'Remove matched element?', type=b'boolean', required=False)
    filter = Attribute(b'Filter by attributes', type=b'function', required=False, default=None)
    _max = Attribute(b'Maximum number of tags to match', type=b'integer', required=False, default=None)

    def logic(self, context):
        select, html = self.get_parameters(context, b'select', b'src')
        if not html.strip():
            self.set_context(context, self.dst(context), b'')
            return
        else:
            let_map = self.get_let_map(context)
            if not html:
                self.set_context(context, self.dst(context), b'')
                return
            try:
                selector = CSSSelector(select)
            except Exception as e:
                self.throw(b'soup.bad-selector', text_type(e))

            html_root = fragment_fromstring(html, create_parent=True)
            append, replace, prepend, remove, _max = self.get_parameters(context, b'append', b'replace', b'prepend', b'remove', b'max')
            if self.has_parameter(b'filter'):
                filter_func = self.filter(context).get_scope_callable(context)
            else:
                filter_func = None
            count = 0
            for el in selector(html_root):
                if filter_func is not None:
                    if not filter_func(el.attrib):
                        continue
                if _max is not None and count >= _max:
                    break
                count += 1
                if let_map:
                    attrib = el.attrib
                    for k, v in let_map.items():
                        if v is None:
                            del attrib[k]
                        else:
                            attrib[k] = text_type(v)

                if append is not None:
                    el.append(fragment_fromstring(append))
                if replace is not None:
                    el.getparent().replace(el, fragment_fromstring(replace))
                if prepend is not None:
                    el.insert(0, fragment_fromstring(prepend))
                if remove:
                    el.getparent().remove(el)

            result_markup = (b'').join(tostring(child).decode(b'utf-8') for child in html_root.getchildren())
            self.set_context(context, self.dst(context), result_markup)
            return


class Extract(DataSetter):
    """
    Extract tags from HTML with CSS selectors

    """
    xmlns = namespaces.soup

    class Help:
        synopsis = b'extract tags from HTML'

    select = Attribute(b'CSS selector', type=b'text', default=b'*')
    src = Attribute(b'HTML document or fragment', type=b'expression', required=True)
    filter = Attribute(b'Filter by attributes', type=b'function', required=False, default=None)
    _max = Attribute(b'Maximum number of tags to match', type=b'integer', required=False, default=None)

    def logic(self, context):
        select, html, filter, _max = self.get_parameters(context, b'select', b'src', b'filter', b'max')
        if not html.strip():
            self.set_result(context, [])
            return
        else:
            try:
                selector = CSSSelector(select)
            except Exception as e:
                self.throw(b'soup.bad-selector', text_type(e))

            html_root = fromstring(html)
            if self.has_parameter(b'filter'):
                filter_func = self.filter(context).get_scope_callable(context)
            else:
                filter_func = None
            elements = []
            count = 0
            for el in selector(html_root):
                if filter_func is not None:
                    if not filter_func(el.attrib):
                        continue
                if _max is not None and count >= _max:
                    break
                count += 1
                elements.append(el)

            self.set_result(context, elements)
            return

    def set_result(self, context, elements):
        result_markup = (b'').join(tostring(el).decode(b'utf-8') for el in elements)
        self.set_context(context, self.dst(context), result_markup)


class ExtractList(Extract):
    """
    Extract a list of markup fragments from HTML

    """
    xmlns = namespaces.soup

    class Help:
        synopsis = b'extract a list of markup fragments from HTML'

    def set_result(self, context, elements):
        result = [ tostring(el).decode(b'utf-8') for el in elements ]
        self.set_context(context, self.dst(context), result)


class ExtractAttrs(Extract):
    """
    Extract attributes from HTML tags

    """
    xmlns = namespaces.soup

    class Help:
        synopsis = b'extract attributes from HTML tags'

    def set_result(self, context, elements):
        result = [ el.attrib for el in elements ]
        self.set_context(context, self.dst(context), result)


class ExtractTags(Extract):
    """
    Extract tag objects from HTML.

    """
    xmlns = namespaces.soup

    class Help:
        synopsis = b'extract elements from HTML tags'

    def set_result(self, context, elements):
        result = [ HTMLTag(el) for el in elements ]
        self.set_context(context, self.dst(context), result)


class ExtractToc(DataSetter):
    """Extract nested headings from HTML fragment."""
    xmlns = namespaces.soup
    src = Attribute(b'HTML document or fragment', type=b'expression', required=True)

    def get_value(self, context):
        html = self.src(context)
        html_root = fragment_fromstring(html, create_parent=True)
        selector = CSSSelector(b'h1,h2,h3,h4,h5,h6,h7')
        root = [
         {b'level': 0, 
            b'children': []}]
        for h in selector(html_root):
            if not h.text:
                continue
            level = int(h.tag.decode(b'utf-8')[1:])
            title = h.text
            if not isinstance(title, text_type):
                title = title.decode(b'utf-8')
            depth = root
            while depth and level > depth[(-1)][b'level']:
                depth = depth[(-1)][b'children']

            depth.append({b'level': level, 
               b'title': title, 
               b'children': []})

        return root[0][b'children']


class AddIdToHeadings(DataSetter):
    """
    Adds automatically generated id attributes to headings.

    """
    xmlns = namespaces.soup
    src = Attribute(b'HTML document or fragment', type=b'expression', missing=False, required=True)
    prefix = Attribute(b'Prefix to add to id', type=b'text', default=b'')

    def get_value(self, context):
        html = self.src(context)
        prefix = self.prefix(context)
        html_root = fragment_fromstring(html, create_parent=True)
        selector = CSSSelector(b'h1,h2,h3,h4,h5,h6,h7')
        for heading in selector(html_root):
            heading.attrib[b'id'] = (b'{}{}').format(prefix, slugify(heading.text.decode(b'utf-8')))

        result_markup = (b'').join(tostring(child).decode(b'utf-8') for child in html_root.getchildren())
        return result_markup


class ExtractData(Extract):
    """
    Extract HTML5 data- attributes

    """
    xmlns = namespaces.soup
    raw = Attribute(b'return raw data (without attempting JSON decode)?', type=b'boolean', default=False)

    class Help:
        synopsis = b'extract HTML5 data attributes from HTML'

    def set_result(self, context, elements):
        all_data = []
        raw = self.raw(context)

        def make_data(v):
            try:
                data = json.loads(v)
            except:
                data = v

            return data

        for el in elements:
            if raw:
                data = {k.partition(b'-')[(-1)]:v for k, v in el.attrib.items() if k.startswith(b'data-') if k.startswith(b'data-')}
            else:
                data = {k.partition(b'-')[(-1)]:make_data(v) for k, v in el.attrib.items() if k.startswith(b'data-')}
            all_data.append(data)

        self.set_context(context, self.dst(context), all_data)