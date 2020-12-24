# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/xml/builder.py
# Compiled at: 2018-05-03 13:55:55
from __future__ import absolute_import
from past.builtins import basestring
from builtins import object
import xml.etree.ElementTree as ET
try:
    from functools import partial
except ImportError:

    def partial(func, tag):
        return lambda *args, **kwargs: func(tag, *args, **kwargs)


try:
    callable
except NameError:

    def callable(f):
        return hasattr(f, '__call__')


try:
    basestring
except NameError:
    basestring = str

try:
    unicode
except NameError:
    unicode = str

class ElementMaker(object):
    """Element generator factory.

    Unlike the ordinary Element factory, the E factory allows you to pass in
    more than just a tag and some optional attributes; you can also pass in
    text and other elements.  The text is added as either text or tail
    attributes, and elements are inserted at the right spot.  Some small
    examples::

        >>> import xml.etree.ElementTree as ET

        >>> ET.tostring(E("tag"))  # doctest: +ALLOW_BYTES 
        b'<tag />'
        >>> ET.tostring(E("tag", "text"))  # doctest: +ALLOW_BYTES
        b'<tag>text</tag>'
        >>> ET.tostring(E("tag", "text", key="value"))  # doctest: +ALLOW_BYTES
        b'<tag key="value">text</tag>'
        >>> ET.tostring(E("tag", E("subtag", "text"), "tail"))  # doctest: +ALLOW_BYTES
        b'<tag><subtag>text</subtag>tail</tag>'

    For simple tags, the factory also allows you to write ``E.tag(...)`` instead
    of ``E('tag', ...)``::

        >>> ET.tostring(E.tag())  # doctest: +ALLOW_BYTES
        b'<tag />'
        >>> ET.tostring(E.tag("text"))  # doctest: +ALLOW_BYTES
        b'<tag>text</tag>'
        >>> ET.tostring(E.tag(E.subtag("text"), "tail"))  # doctest: +ALLOW_BYTES
        b'<tag><subtag>text</subtag>tail</tag>'

    Here's a somewhat larger example; this shows how to generate HTML
    documents, using a mix of prepared factory functions for inline elements,
    nested ``E.tag`` calls, and embedded XHTML fragments::

        # some common inline elements
        A = E.a
        I = E.i
        B = E.b

        def CLASS(v):
            # helper function, 'class' is a reserved word
            return {'class': v}

        page = (
            E.html(
                E.head(
                    E.title("This is a sample document")
                ),
                E.body(
                    E.h1("Hello!", CLASS("title")),
                    E.p("This is a paragraph with ", B("bold"), " text in it!"),
                    E.p("This is another paragraph, with a ",
                        A("link", href="http://www.python.org"), "."),
                    E.p("Here are some reservered characters: <spam&egg>."),
                    ET.XML("<p>And finally, here is an embedded XHTML fragment.</p>"),
                )
            )
        )

        print ET.tostring(page)

    Here's a prettyprinted version of the output from the above script::

        <html>
          <head>
            <title>This is a sample document</title>
          </head>
          <body>
            <h1 class="title">Hello!</h1>
            <p>This is a paragraph with <b>bold</b> text in it!</p>
            <p>This is another paragraph, with <a href="http://www.python.org">link</a>.</p>
            <p>Here are some reservered characters: &lt;spam&amp;egg&gt;.</p>
            <p>And finally, here is an embedded XHTML fragment.</p>
          </body>
        </html>
    """

    def __init__(self, typemap=None, namespace=None, makeelement=None):
        if namespace is not None:
            self._namespace = '{' + namespace + '}'
        else:
            self._namespace = None
        if makeelement is not None:
            assert callable(makeelement)
            self._makeelement = makeelement
        else:
            self._makeelement = ET.Element
        if typemap:
            typemap = typemap.copy()
        else:
            typemap = {}

        def add_text(elem, item):
            try:
                elem[(-1)].tail = (elem[(-1)].tail or '') + item
            except IndexError:
                elem.text = (elem.text or '') + item

        def add_cdata(elem, cdata):
            if elem.text:
                raise ValueError("Can't add a CDATA section. Element already has some text: %r" % elem.text)
            elem.text = cdata

        if str not in typemap:
            typemap[str] = add_text
        if unicode not in typemap:
            typemap[unicode] = add_text

        def add_dict(elem, item):
            attrib = elem.attrib
            for k, v in list(item.items()):
                if isinstance(v, basestring):
                    attrib[k] = v
                else:
                    attrib[k] = typemap[type(v)](None, v)

            return

        if dict not in typemap:
            typemap[dict] = add_dict
        self._typemap = typemap
        return

    def __call__(self, tag, *children, **attrib):
        get = self._typemap.get
        if self._namespace is not None and tag[0] != '{':
            tag = self._namespace + tag
        elem = self._makeelement(tag)
        if attrib:
            get(dict)(elem, attrib)
        for item in children:
            if callable(item):
                item = item()
            t = get(type(item))
            if t is None:
                if ET.iselement(item):
                    elem.append(item)
                    continue
                for basetype in type(item).__mro__:
                    t = get(basetype)
                    if t is not None:
                        break
                else:
                    raise TypeError('bad argument type: %s(%r)' % (
                     type(item).__name__, item))

            v = t(elem, item)
            if v:
                get(type(v))(elem, v)

        return elem

    def __getattr__(self, tag):
        return partial(self, tag)


E = ElementMaker()