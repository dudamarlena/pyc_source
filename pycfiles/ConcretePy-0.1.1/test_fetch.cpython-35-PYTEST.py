# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_fetch.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 2408 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from concrete.util import CommunicationContainerFetchHandler, RelayFetchHandler
from concrete.util import FetchCommunicationClientWrapper, SubprocessFetchCommunicationServiceWrapper
from concrete.util import FetchBackedCommunicationContainer
from concrete.util import find_port
from concrete.util import create_comm
from concrete.validate import validate_communication

def test_comm_container_fetch_handler():
    comm_container = {'one': create_comm('one'), 
     'two': create_comm('two')}
    impl = CommunicationContainerFetchHandler(comm_container)
    host = 'localhost'
    port = find_port()
    with SubprocessFetchCommunicationServiceWrapper(impl, host, port):
        with FetchCommunicationClientWrapper(host, port) as (cli):
            @py_assert1 = cli.getCommunicationCount
            @py_assert3 = @py_assert1()
            if not @py_assert3:
                @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getCommunicationCount\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(cli) if 'cli' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cli) else 'cli', 'py4': @pytest_ar._saferepr(@py_assert3)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format5))
            @py_assert1 = @py_assert3 = None
            ids = cli.getCommunicationIDs(0, 10)
            @py_assert0 = 'one'
            @py_assert2 = @py_assert0 in ids
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, ids)) % {'py3': @pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids', 'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            @py_assert0 = 'two'
            @py_assert2 = @py_assert0 in ids
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, ids)) % {'py3': @pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids', 'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None
            @py_assert0 = 'foo'
            @py_assert2 = @py_assert0 not in ids
            if not @py_assert2:
                @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, ids)) % {'py3': @pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids', 'py1': @pytest_ar._saferepr(@py_assert0)}
                @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                raise AssertionError(@pytest_ar._format_explanation(@py_format6))
            @py_assert0 = @py_assert2 = None


def test_fetch_backed_container():
    comm_container = {'one': create_comm('one'), 
     'two': create_comm('two')}
    impl = CommunicationContainerFetchHandler(comm_container)
    host = 'localhost'
    port = find_port()
    with SubprocessFetchCommunicationServiceWrapper(impl, host, port):
        cc = FetchBackedCommunicationContainer(host, port)
        @py_assert2 = len(cc)
        @py_assert5 = 2
        @py_assert4 = @py_assert2 == @py_assert5
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py6': @pytest_ar._saferepr(@py_assert5), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        @py_assert0 = 'one'
        @py_assert2 = @py_assert0 in cc
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cc)) % {'py3': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = 'two'
        @py_assert2 = @py_assert0 in cc
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, cc)) % {'py3': @pytest_ar._saferepr(cc) if 'cc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cc) else 'cc', 'py1': @pytest_ar._saferepr(@py_assert0)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        for comm_id in cc:
            comm = cc[comm_id]
            @py_assert2 = validate_communication(comm)
            if not @py_assert2:
                @py_format4 = ('' + 'assert %(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n}') % {'py0': @pytest_ar._saferepr(validate_communication) if 'validate_communication' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validate_communication) else 'validate_communication', 'py3': @pytest_ar._saferepr(@py_assert2), 'py1': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
                raise AssertionError(@pytest_ar._format_explanation(@py_format4))
            @py_assert2 = None


def test_relay_container_fetch_handler():
    comm_container = {'one': create_comm('one'), 
     'two': create_comm('two')}
    impl = CommunicationContainerFetchHandler(comm_container)
    host = 'localhost'
    port = find_port()
    with SubprocessFetchCommunicationServiceWrapper(impl, host, port):
        relay_impl = RelayFetchHandler(host, port)
        relay_host = 'localhost'
        relay_port = find_port()
        with SubprocessFetchCommunicationServiceWrapper(relay_impl, relay_host, relay_port):
            with FetchCommunicationClientWrapper(relay_host, relay_port) as (cli):
                @py_assert1 = cli.getCommunicationCount
                @py_assert3 = @py_assert1()
                if not @py_assert3:
                    @py_format5 = ('' + 'assert %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.getCommunicationCount\n}()\n}') % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(cli) if 'cli' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cli) else 'cli', 'py4': @pytest_ar._saferepr(@py_assert3)}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format5))
                @py_assert1 = @py_assert3 = None
                ids = cli.getCommunicationIDs(0, 10)
                @py_assert0 = 'one'
                @py_assert2 = @py_assert0 in ids
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, ids)) % {'py3': @pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids', 'py1': @pytest_ar._saferepr(@py_assert0)}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                @py_assert0 = 'two'
                @py_assert2 = @py_assert0 in ids
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, ids)) % {'py3': @pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids', 'py1': @pytest_ar._saferepr(@py_assert0)}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None
                @py_assert0 = 'foo'
                @py_assert2 = @py_assert0 not in ids
                if not @py_assert2:
                    @py_format4 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py3)s', ), (@py_assert0, ids)) % {'py3': @pytest_ar._saferepr(ids) if 'ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ids) else 'ids', 'py1': @pytest_ar._saferepr(@py_assert0)}
                    @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
                    raise AssertionError(@pytest_ar._format_explanation(@py_format6))
                @py_assert0 = @py_assert2 = None