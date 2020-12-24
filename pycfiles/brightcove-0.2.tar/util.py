# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/brightcontent/util.py
# Compiled at: 2006-09-01 13:29:17
import amara

def fixup_namespaces(node):
    """
    reduces namespace clutter in documents by looking for duplicate namespace
    declarations and preferring those set as document prefixes
    """
    doc = node.rootNode
    nss = dict(zip(doc.xmlns_prefixes.values(), doc.xmlns_prefixes.keys()))
    if node.namespaceURI in nss:
        node.xmlnsPrefix = nss[node.namespaceURI]
        node.nodeName = node.prefix and node.prefix + ':' + node.localName or node.localName
    for child in node.xml_xpath('*'):
        fixup_namespaces(child)


def quick_xml_scan(source, field, **kwargs):
    val = unicode(amara.pushbind(source, field, **kwargs).next())
    return val


class node_wrapper:
    __module__ = __name__

    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return iter([self.node.xml()])


def get_base_url(environ):
    from urllib import quote
    url = environ['wsgi.url_scheme'] + '://'
    if environ.get('HTTP_HOST'):
        url += environ['HTTP_HOST']
    else:
        url += environ['SERVER_NAME']
        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
                url += ':' + environ['SERVER_PORT']
        elif environ['SERVER_PORT'] != '80':
            url += ':' + environ['SERVER_PORT']
    url += quote(environ.get('SCRIPT_NAME', '')) + '/'
    return url