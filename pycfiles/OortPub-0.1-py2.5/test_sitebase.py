# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/test/test_sitebase.py
# Compiled at: 2007-09-30 15:53:27
from rdflib import ConjunctiveGraph
from oort.sitebase import MultiBaseResourceViewer, AspectBase

class TestResourceViewerBase:
    pass


def test_MultiBaseResourceViewer():

    class TestViewer(MultiBaseResourceViewer):
        resourceBases = {'ont': ('http://example.org/rdfns/ontology#', ''), 
           'ex': ('http://example.org/resources/', '/'), 
           'urn': ('urn:example-org:', ':')}
        defaultResource = 'http://example.org/default/resource'

    viewer = TestViewer(ConjunctiveGraph())

    def test_path(path, expected, samePath=True):
        resource = viewer.resource_from(path.split('/'))
        assert resource == expected
        (path2, _success) = viewer.resource_to_app_path(resource)
        assert (path == path2) is samePath

    test_path('ex/path/to/resource', 'http://example.org/resources/path/to/resource')
    test_path('ex/', 'http://example.org/resources/')
    test_path('ont/OneConcept', 'http://example.org/rdfns/ontology#OneConcept')
    test_path('ont/someRelationTo', 'http://example.org/rdfns/ontology#someRelationTo')
    test_path('bad/nothing/to/see/here', 'http://example.org/default/resource', False)
    test_path('bad/', 'http://example.org/default/resource', False)
    test_path('/', 'http://example.org/default/resource', False)
    test_path('', 'http://example.org/default/resource', False)


def test_using():
    dummy = object()
    aspect = AspectBase(None)
    assert aspect == aspect.using(item=dummy)
    assert aspect.queries['item'] == dummy
    return