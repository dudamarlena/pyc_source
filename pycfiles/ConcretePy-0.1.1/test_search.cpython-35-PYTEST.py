# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_search.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 2076 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TCompactProtocol
from concrete.util import SubprocessSearchServiceWrapper
from concrete.util import find_port
from time import time
from concrete.search import SearchService
from concrete import SearchType, SearchQuery, SearchResult, SearchResultItem
from concrete import UUID
from concrete import AnnotationMetadata

class FooSearch(SearchService.Iface):
    METADATA_TOOL = 'Foo Search'

    def search(self, search_query):
        return SearchResult(uuid=UUID(uuidString='12345678-1234-5678-1234-567812345678'), searchResultItems=[SearchResultItem(communicationId=term, score=42.0) for term in search_query.terms], metadata=AnnotationMetadata(tool=self.METADATA_TOOL, timestamp=int(time())))

    def shutdown(self):
        pass


def test_search_communications():
    impl = FooSearch()
    host = 'localhost'
    port = find_port()
    timeout = 5
    terms = [
     'foo', 'bar']
    query = SearchQuery(type=SearchType.COMMUNICATIONS, terms=[t for t in terms])
    with SubprocessSearchServiceWrapper(impl, host, port, timeout=timeout):
        transport = TSocket.TSocket(host, port)
        transport = TTransport.TFramedTransport(transport)
        protocol = TCompactProtocol.TCompactProtocolAccelerated(transport)
        cli = SearchService.Client(protocol)
        transport.open()
        res = cli.search(query)
        transport.close()
        @py_assert1 = res.uuid
        @py_assert3 = @py_assert1.uuidString
        @py_assert6 = '12345678-1234-5678-1234-567812345678'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.uuid\n}.uuidString\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert2 = res.searchResultItems
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.searchResultItems\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert0 = res.searchResultItems[0]
        @py_assert2 = @py_assert0.communicationId
        @py_assert5 = 'foo'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.communicationId\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = res.searchResultItems[0]
        @py_assert2 = @py_assert0.score
        @py_assert5 = 42.0
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.score\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = res.searchResultItems[1]
        @py_assert2 = @py_assert0.communicationId
        @py_assert5 = 'bar'
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.communicationId\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = res.searchResultItems[1]
        @py_assert2 = @py_assert0.score
        @py_assert5 = 42.0
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.score\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert1 = res.metadata
        @py_assert3 = @py_assert1.tool
        @py_assert6 = 'Foo Search'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.metadata\n}.tool\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None