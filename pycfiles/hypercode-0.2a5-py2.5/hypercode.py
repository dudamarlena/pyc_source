# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/hypercode.py
# Compiled at: 2008-03-19 23:14:57
"""

http://www.python.org/dev/peps/pep-0302/

http://svn.python.org/projects/sandbox/trunk/import_in_py

hypercode.dotted_name(uri)
hypercode.uri(dotted_name)

dotted name to/from URLRef

"""
import sys, types, os
from urllib2 import urlopen, Request, URLError
from urlparse import urlparse
from urlparse import urljoin, urldefrag
from urllib import pathname2url, url2pathname
import inspect
from rdf.term import URIRef, BNode, Literal
from rdf.term import Namespace, RDF, RDFS
from rdf.graph import Graph
__version__ = '0.2a5'
PYTHON = Namespace('tag:eikeon@eikeon.com,2008-02:python#')
headers = {'Accept': 'text/python', 
   'User-agent': 'hc_import-%s (eikeon@eikeon.com)' % __version__}
uri_map = set()

def map(logical, physical):
    """Map all URIRefs starting with logical to corresponding ones starting with physical."""
    if isinstance(physical, types.ModuleType):
        logical = URIRef(logical).defrag()
        sys.modules[logical] = physical
    else:
        physical = _absolutize(physical)
        uri_map.add((logical, physical))


def get_physical(uri):
    """Concert from logical uri to physical uri"""
    for (logical, physical) in uri_map:
        if uri.startswith(logical):
            return URIRef(uri.replace(logical, physical, 1))


def _absolutize(uri, defrag=False):
    """
    TODO:
    """
    base = urljoin('file:', pathname2url(os.getcwd()))
    result = urljoin('%s/' % base, uri, allow_fragments=not defrag)
    if defrag:
        result = urldefrag(result)[0]
    if not defrag:
        if uri and uri[(-1)] == '#' and result[(-1)] != '#':
            result = '%s#' % result
    return URIRef(result)


def import_(logical):
    logical = URIRef(logical)
    module_uri = logical.defrag()
    module = sys.modules.get(module_uri, None)
    if module is None:
        physical = _absolutize(get_physical(logical) or logical).defrag()
        if not physical.endswith('.py'):
            physical = URIRef('%s.py' % physical)
        req = Request(physical, None, headers)
        try:
            f = urlopen(req)
            value = f.read()
        except URLError, e:
            raise Exception("Could not import '%s' from '%s': %r" % (logical, physical, e))
        else:
            safe_module_name = '__uri___%s' % hash(module_uri)
            module = types.ModuleType(safe_module_name)
            module.__name__ = module_uri
            module.__file__ = physical
            module.__ispkg__ = 0
            sys.modules[module_uri] = module
            module.__dict__.update()
            value = value.replace('\r\n', '\n')
            value = value.replace('\r', '\n')
            c = compile(value + '\n', module_uri, 'exec')
            exec c in module.__dict__
    if '#' in logical:
        name = logical.split('#', 1)[(-1)]
        return getattr(module, name)
    else:
        return module
    return


def rdf(uri):
    module = import_(uri)
    module_uri = URIRef(module.__name__)
    g = Graph()
    g.bind('python', PYTHON.uri)
    g.bind('m', URIRef('%s#' % module_uri))
    g.add((module_uri, RDF.type, PYTHON['Module']))
    g.add((module_uri, RDFS.label, Literal(module.__name__)))
    g.add((module_uri, RDFS.comment, Literal(module.__doc__ or '')))
    for (name, m) in inspect.getmembers(module):
        if inspect.isclass(m):
            uri = URIRef('#%s' % name, base=module_uri)
            g.add((uri, RDF.type, PYTHON['Class']))
            g.add((uri, RDFS.label, Literal(name)))
            g.add((uri, RDFS.comment, Literal(m.__doc__ or '')))
            g.add((module_uri, PYTHON['defines'], uri))
            for (attr_name, kind, class_, object_) in inspect.classify_class_attrs(m):
                attr_uri = URIRef('#%s.%s' % (name, attr_name))
                g.add((attr_uri, RDF.type, PYTHON[kind]))
                g.add((attr_uri, RDFS.label, Literal(attr_name)))
                g.add((attr_uri, RDFS.comment, Literal('%s' % object_.__doc__)))
                g.add((uri, PYTHON['defines'], attr_uri))

    return g


if __name__ == '__main__':
    c = import_('http://localhost:8080/handlers#Element')
    print c