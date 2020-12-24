# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/integration-tests/test_annotate.py
# Compiled at: 2017-07-18 13:12:53
# Size of source mod 2**32: 2715 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TCompactProtocol
from concrete.util import SubprocessAnnotateCommunicationServiceWrapper
from concrete.util import find_port
from concrete.util import create_comm
from time import time
from concrete.annotate import AnnotateCommunicationService
from concrete import AnnotationMetadata

class NoopAnnotateCommunicationService(AnnotateCommunicationService.Iface):
    METADATA_TOOL = 'No-op AnnotateCommunicationService'

    def annotate(self, communication):
        return communication

    def getMetadata(self):
        metadata = AnnotationMetadata(tool=self.METADATA_TOOL, timestamp=int(time()))
        return metadata

    def getDocumentation(self):
        return '        AnnotateCommunicationService that returns communication unmodified\n        '

    def shutdown(self):
        pass


def test_annotate():
    impl = NoopAnnotateCommunicationService()
    host = 'localhost'
    port = find_port()
    timeout = 5
    comm_id = '1-2-3-4'
    comm = create_comm(comm_id)
    comm_uuid_uuidString = comm.uuid.uuidString
    comm_metadata_tool = comm.metadata.tool
    comm_metadata_timestamp = comm.metadata.timestamp
    with SubprocessAnnotateCommunicationServiceWrapper(impl, host, port, timeout=timeout):
        transport = TSocket.TSocket(host, port)
        transport = TTransport.TFramedTransport(transport)
        protocol = TCompactProtocol.TCompactProtocolAccelerated(transport)
        cli = AnnotateCommunicationService.Client(protocol)
        transport.open()
        res = cli.annotate(comm)
        transport.close()
        @py_assert1 = res.id
        @py_assert3 = @py_assert1 == comm_id
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py4)s', ), (@py_assert1, comm_id)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py4': @pytest_ar._saferepr(comm_id) if 'comm_id' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_id) else 'comm_id'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = res.uuid
        @py_assert3 = @py_assert1.uuidString
        @py_assert5 = @py_assert3 == comm_uuid_uuidString
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.uuid\n}.uuidString\n} == %(py6)s', ), (@py_assert3, comm_uuid_uuidString)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py6': @pytest_ar._saferepr(comm_uuid_uuidString) if 'comm_uuid_uuidString' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_uuid_uuidString) else 'comm_uuid_uuidString', 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = res.metadata
        @py_assert3 = @py_assert1.tool
        @py_assert5 = @py_assert3 == comm_metadata_tool
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.metadata\n}.tool\n} == %(py6)s', ), (@py_assert3, comm_metadata_tool)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py6': @pytest_ar._saferepr(comm_metadata_tool) if 'comm_metadata_tool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_metadata_tool) else 'comm_metadata_tool', 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = res.metadata
        @py_assert3 = @py_assert1.timestamp
        @py_assert5 = @py_assert3 == comm_metadata_timestamp
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.metadata\n}.timestamp\n} == %(py6)s', ), (@py_assert3, comm_metadata_timestamp)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(res) if 'res' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(res) else 'res', 'py6': @pytest_ar._saferepr(comm_metadata_timestamp) if 'comm_metadata_timestamp' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm_metadata_timestamp) else 'comm_metadata_timestamp', 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


def test_get_metadata():
    impl = NoopAnnotateCommunicationService()
    host = 'localhost'
    port = find_port()
    timeout = 5
    with SubprocessAnnotateCommunicationServiceWrapper(impl, host, port, timeout=timeout):
        transport = TSocket.TSocket(host, port)
        transport = TTransport.TFramedTransport(transport)
        protocol = TCompactProtocol.TCompactProtocolAccelerated(transport)
        cli = AnnotateCommunicationService.Client(protocol)
        transport.open()
        metadata = cli.getMetadata()
        transport.close()
        @py_assert1 = NoopAnnotateCommunicationService.METADATA_TOOL
        @py_assert5 = metadata.tool
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.METADATA_TOOL\n} == %(py6)s\n{%(py6)s = %(py4)s.tool\n}', ), (@py_assert1, @py_assert5)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py0': @pytest_ar._saferepr(NoopAnnotateCommunicationService) if 'NoopAnnotateCommunicationService' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(NoopAnnotateCommunicationService) else 'NoopAnnotateCommunicationService', 'py6': @pytest_ar._saferepr(@py_assert5), 'py4': @pytest_ar._saferepr(metadata) if 'metadata' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(metadata) else 'metadata'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None