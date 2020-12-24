# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/TagRenderer.py
# Compiled at: 2010-03-01 05:51:20
"""

Tool Server Framework - generate HTML and XML code with Python

Copyright (c) 2002, Georg Bauer <gb@rfc1437.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from Toolserver.Utils import quote
from Toolserver.Config import config

class Tag:

    def __init__(self, tagname, namespace=''):
        self._name = tagname
        self._namespace = namespace
        if namespace:
            self._tag = '%s:%s' % (namespace, tagname)
        else:
            self._tag = tagname

    def _flatten(self, l):
        r = []
        for e in l:
            if type(e) in (type([]), type(())):
                r.extend(self._flatten(e))
            else:
                r.append(str(e))

        return r

    def _attrname(self, attrname):
        if attrname.find('__') > 0:
            (namespace, attrname) = attrname.split('__', 1)
            return namespace + ':' + attrname.replace('_', '-')
        else:
            return attrname.replace('_', '-')

    def _attrlist(self, attrs):
        return (' ').join(map(lambda k: '%s="%s"' % (self._attrname(k), quote(attrs[k])), attrs.keys()))

    def __call__(self, *content, **attrs):
        attrs = self._attrlist(attrs)
        if content:
            content = ('').join(self._flatten(content))
            if attrs:
                return '<%s %s>%s</%s>' % (self._tag, attrs, content, self._tag)
            return '<%s>%s</%s>' % (self._tag, content, self._tag)
        else:
            if attrs:
                return '<%s %s />' % (self._tag, attrs)
            else:
                return '<%s />' % self._tag


class HTMLTag(Tag):

    def __call__(self, *content, **attrs):
        if content:
            return Tag.__call__(self, *content, **attrs)
        else:
            attrs = self._attrlist(attrs)
            if attrs:
                return '<%s %s>' % (self._tag, attrs)
            return '<%s>' % self._tag


class DocTypedTag(Tag):

    def __init__(self, tagname, namespace, doctype=None):
        Tag.__init__(self, tagname, namespace)
        if doctype:
            self._doctype = doctype

    def __call__(self, *content, **attrs):
        s = self._doctype + '\n' + Tag.__call__(self, *content, **attrs)
        return s


class DocTypedAndNameSpacedTag(DocTypedTag):

    def __init__(self, tagname, namespace, doctype=None, namespaces=None):
        DocTypedTag.__init__(self, tagname, namespace, doctype)
        self._namespaces = namespaces

    def __call__(self, *content, **attrs):
        if self._namespaces:
            for ns in self._namespaces.keys():
                attrs['xmlns__%s' % ns] = self._namespaces[ns]

        s = DocTypedTag.__call__(self, *content, **attrs)
        return s


class TagLibrary:
    _doctype = ''
    _toplevel = ''
    _tagclass = Tag
    _topleveltagclass = DocTypedTag

    def __init__(self, namespace=''):
        self._namespace = namespace

    def __getattr__(self, key):
        return self._tag(key)

    def _tag(self, tagname):
        if tagname.lower() == self._toplevel.lower():
            return self._topleveltagclass(tagname, self._namespace, self._doctype)
        else:
            return self._tagclass(tagname, self._namespace)


class XMLTagLibrary(TagLibrary):
    _doctype = '<?xml version="1.0" encoding="%s"?>' % config.documentEncoding
    _toplevel = 'xml'
    _knownnamespaces = (('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'), )
    _topleveltagclass = DocTypedAndNameSpacedTag

    def __init__(self, namespace, namespaces, othernamespaces):
        TagLibrary.__init__(self, namespace)
        self._namespaces = {}
        for ns in othernamespaces.keys():
            self._namespaces[ns] = othernamespaces[ns]

        for (nsname, nsurl) in self._knownnamespaces:
            if nsname in namespaces:
                self._namespaces[nsname] = nsurl

    def _tag(self, tagname):
        if tagname.lower() == self._toplevel.lower():
            if self._namespaces:
                return self._topleveltagclass(tagname, self._namespace, self._doctype, self._namespaces)
            else:
                return TagLibrary._tag(self, tagname)
        else:
            return TagLibrary._tag(self, tagname)


class HTMLTagLibrary(TagLibrary):
    _doctype = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'
    _toplevel = 'html'
    _tagclass = HTMLTag

    def head(self, *args, **kw):
        args = args + (self.meta(http_equiv='Content-type', content='text/html', charset=config.documentEncoding),)
        return apply(self._tag('head'), args, kw)


class RSSTagLibrary(TagLibrary):
    _doctype = '<?xml version="1.0" encoding="%s"?>' % config.documentEncoding
    _toplevel = 'rss'


class RSS2TagLibrary(XMLTagLibrary):
    _toplevel = 'rss'
    _knownnamespaces = XMLTagLibrary._knownnamespaces + (
     ('trackback', 'http://madskills.com/public/xml/rss/module/trackback'),
     ('ent', 'http://www.purl.org/NET/ENT/1.0/'))

    def __init__(self, namespaces, othernamespaces):
        XMLTagLibrary.__init__(self, '', namespaces, othernamespaces)

    def rss(self, *args, **kw):
        if not kw.has_key('version'):
            kw['version'] = '2.0'
        return apply(self._tag('rss'), args, kw)


class XMLDocTagLibrary(XMLTagLibrary):

    def __init__(self, toplevel, namespaces, othernamespaces):
        XMLTagLibrary.__init__(self, '', namespaces, othernamespaces)
        self._toplevel = toplevel


html = HTMLTagLibrary()
rss = RSSTagLibrary()

def namespace(namespace):
    return TagLibrary(namespace)


def rss2(*namespaces, **othernamespaces):
    return RSS2TagLibrary(namespaces, othernamespaces)


def xml(toplevel, *namespaces, **othernamespaces):
    return XMLDocTagLibrary(toplevel, namespaces, othernamespaces)