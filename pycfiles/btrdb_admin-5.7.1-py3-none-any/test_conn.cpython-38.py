# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/btrdb/test_conn.py
# Compiled at: 2019-09-25 10:27:08
# Size of source mod 2**32: 8265 bytes
__doc__ = '\nTesting package for the btrdb connection module\n'
import uuid as uuidlib, pytest
from unittest.mock import Mock, PropertyMock, patch, call
from btrdb.conn import Connection, BTrDB
from btrdb.endpoint import Endpoint
from btrdb.grpcinterface import btrdb_pb2
from btrdb.exceptions import *

class TestConnection(object):

    def test_raises_err_invalid_address--- This code section failed: ---

 L.  37         0  LOAD_STR                 '127.0.0.1::4410'
                2  STORE_FAST               'address'

 L.  38         4  LOAD_GLOBAL              pytest
                6  LOAD_METHOD              raises
                8  LOAD_GLOBAL              ValueError
               10  CALL_METHOD_1         1  ''
               12  SETUP_WITH           28  'to 28'
               14  STORE_FAST               'exc'

 L.  39        16  LOAD_GLOBAL              Connection
               18  LOAD_FAST                'address'
               20  CALL_FUNCTION_1       1  ''
               22  STORE_FAST               'conn'
               24  POP_BLOCK        
               26  BEGIN_FINALLY    
             28_0  COME_FROM_WITH       12  '12'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

 L.  40        34  LOAD_STR                 'expecting address:port'
               36  LOAD_GLOBAL              str
               38  LOAD_FAST                'exc'
               40  CALL_FUNCTION_1       1  ''
               42  COMPARE_OP               in
               44  POP_JUMP_IF_TRUE     50  'to 50'
               46  LOAD_ASSERT              AssertionError
               48  RAISE_VARARGS_1       1  ''
             50_0  COME_FROM            44  '44'

Parse error at or near `BEGIN_FINALLY' instruction at offset 26

    def test_raises_err_for_apikey_insecure_port--- This code section failed: ---

 L.  47         0  LOAD_STR                 '127.0.0.1:4410'
                2  STORE_FAST               'address'

 L.  48         4  LOAD_GLOBAL              pytest
                6  LOAD_METHOD              raises
                8  LOAD_GLOBAL              ValueError
               10  CALL_METHOD_1         1  ''
               12  SETUP_WITH           32  'to 32'
               14  STORE_FAST               'exc'

 L.  49        16  LOAD_GLOBAL              Connection
               18  LOAD_FAST                'address'
               20  LOAD_STR                 'abcd'
               22  LOAD_CONST               ('apikey',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'conn'
               28  POP_BLOCK        
               30  BEGIN_FINALLY    
             32_0  COME_FROM_WITH       12  '12'
               32  WITH_CLEANUP_START
               34  WITH_CLEANUP_FINISH
               36  END_FINALLY      

 L.  50        38  LOAD_STR                 'cannot use an API key with an insecure'
               40  LOAD_GLOBAL              str
               42  LOAD_FAST                'exc'
               44  CALL_FUNCTION_1       1  ''
               46  COMPARE_OP               in
               48  POP_JUMP_IF_TRUE     54  'to 54'
               50  LOAD_ASSERT              AssertionError
               52  RAISE_VARARGS_1       1  ''
             54_0  COME_FROM            48  '48'

Parse error at or near `BEGIN_FINALLY' instruction at offset 30


class TestBTrDB(object):

    def test_streams_raises_err_if_version_not_list--- This code section failed: ---

 L.  67         0  LOAD_GLOBAL              BTrDB
                2  LOAD_CONST               None
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'db'

 L.  68         8  LOAD_GLOBAL              pytest
               10  LOAD_METHOD              raises
               12  LOAD_GLOBAL              TypeError
               14  CALL_METHOD_1         1  ''
               16  SETUP_WITH           38  'to 38'
               18  STORE_FAST               'exc'

 L.  69        20  LOAD_FAST                'db'
               22  LOAD_ATTR                streams
               24  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
               26  LOAD_STR                 '2,2'
               28  LOAD_CONST               ('versions',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_WITH       16  '16'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L.  71        44  LOAD_STR                 'versions argument must be of type list'
               46  LOAD_GLOBAL              str
               48  LOAD_FAST                'exc'
               50  CALL_FUNCTION_1       1  ''
               52  COMPARE_OP               in
               54  POP_JUMP_IF_TRUE     60  'to 60'
               56  LOAD_ASSERT              AssertionError
               58  RAISE_VARARGS_1       1  ''
             60_0  COME_FROM            54  '54'

Parse error at or near `BEGIN_FINALLY' instruction at offset 36

    def test_streams_raises_err_if_version_argument_mismatch--- This code section failed: ---

 L.  78         0  LOAD_GLOBAL              BTrDB
                2  LOAD_CONST               None
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'db'

 L.  79         8  LOAD_GLOBAL              pytest
               10  LOAD_METHOD              raises
               12  LOAD_GLOBAL              ValueError
               14  CALL_METHOD_1         1  ''
               16  SETUP_WITH           42  'to 42'
               18  STORE_FAST               'exc'

 L.  80        20  LOAD_FAST                'db'
               22  LOAD_ATTR                streams
               24  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
               26  LOAD_CONST               2
               28  LOAD_CONST               2
               30  BUILD_LIST_2          2 
               32  LOAD_CONST               ('versions',)
               34  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               36  POP_TOP          
               38  POP_BLOCK        
               40  BEGIN_FINALLY    
             42_0  COME_FROM_WITH       16  '16'
               42  WITH_CLEANUP_START
               44  WITH_CLEANUP_FINISH
               46  END_FINALLY      

 L.  82        48  LOAD_STR                 'versions does not match identifiers'
               50  LOAD_GLOBAL              str
               52  LOAD_FAST                'exc'
               54  CALL_FUNCTION_1       1  ''
               56  COMPARE_OP               in
               58  POP_JUMP_IF_TRUE     64  'to 64'
               60  LOAD_ASSERT              AssertionError
               62  RAISE_VARARGS_1       1  ''
             64_0  COME_FROM            58  '58'

Parse error at or near `BEGIN_FINALLY' instruction at offset 40

    def test_streams_stores_versions(self):
        """
        Assert streams correctly stores supplied version info
        """
        db = BTrDB(None)
        uuid1 = uuidlib.UUID'0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
        uuid2 = uuidlib.UUID'17dbe387-89ea-42b6-864b-f505cdb483f5'
        versions = [22, 44]
        expected = dict(zip([uuid1, uuid2], versions))
        streams = db.streams(uuid1, uuid2, versions=versions)
        assert streams._pinned_versions == expected

    @patch('btrdb.conn.BTrDB.stream_from_uuid')
    def test_streams_recognizes_uuid(self, mock_func):
        """
        Assert streams recognizes uuid strings
        """
        db = BTrDB(None)
        uuid1 = uuidlib.UUID'0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
        mock_func.return_value = [1]
        db.streamsuuid1
        mock_func.assert_called_once()
        assert mock_func.call_args[0][0] == uuid1

    @patch('btrdb.conn.BTrDB.stream_from_uuid')
    def test_streams_recognizes_uuid_string(self, mock_func):
        """
        Assert streams recognizes uuid strings
        """
        db = BTrDB(None)
        uuid1 = '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
        mock_func.return_value = [1]
        db.streamsuuid1
        mock_func.assert_called_once()
        assert mock_func.call_args[0][0] == uuid1

    @patch('btrdb.conn.BTrDB.streams_in_collection')
    def test_streams_handles_path(self, mock_func):
        """
        Assert streams calls streams_in_collection for collection/name paths
        """
        db = BTrDB(None)
        ident = 'zoo/animal/dog'
        mock_func.return_value = [1]
        db.streams(ident, '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        mock_func.assert_called_once()
        assert mock_func.call_args[0][0] == 'zoo/animal'
        assert mock_func.call_args[1] == {'tags': {'name': 'dog'}}

    @patch('btrdb.conn.BTrDB.streams_in_collection')
    def test_streams_raises_err--- This code section failed: ---

 L. 147         0  LOAD_GLOBAL              BTrDB
                2  LOAD_CONST               None
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'db'

 L. 148         8  LOAD_STR                 'zoo/animal/dog'
               10  STORE_FAST               'ident'

 L. 150        12  BUILD_LIST_0          0 
               14  LOAD_FAST                'mock_func'
               16  STORE_ATTR               return_value

 L. 151        18  LOAD_GLOBAL              pytest
               20  LOAD_METHOD              raises
               22  LOAD_GLOBAL              NotFound
               24  CALL_METHOD_1         1  ''
               26  SETUP_WITH           44  'to 44'
               28  STORE_FAST               'exc'

 L. 152        30  LOAD_FAST                'db'
               32  LOAD_METHOD              streams
               34  LOAD_FAST                'ident'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          
               40  POP_BLOCK        
               42  BEGIN_FINALLY    
             44_0  COME_FROM_WITH       26  '26'
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  END_FINALLY      

 L. 154        50  LOAD_CONST               1
               52  LOAD_CONST               2
               54  BUILD_LIST_2          2 
               56  LOAD_FAST                'mock_func'
               58  STORE_ATTR               return_value

 L. 155        60  LOAD_GLOBAL              pytest
               62  LOAD_METHOD              raises
               64  LOAD_GLOBAL              NotFound
               66  CALL_METHOD_1         1  ''
               68  SETUP_WITH           86  'to 86'
               70  STORE_FAST               'exc'

 L. 156        72  LOAD_FAST                'db'
               74  LOAD_METHOD              streams
               76  LOAD_FAST                'ident'
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          
               82  POP_BLOCK        
               84  BEGIN_FINALLY    
             86_0  COME_FROM_WITH       68  '68'
               86  WITH_CLEANUP_START
               88  WITH_CLEANUP_FINISH
               90  END_FINALLY      

 L. 159        92  LOAD_CONST               1
               94  BUILD_LIST_1          1 
               96  LOAD_FAST                'mock_func'
               98  STORE_ATTR               return_value

 L. 160       100  LOAD_FAST                'db'
              102  LOAD_METHOD              streams
              104  LOAD_FAST                'ident'
              106  CALL_METHOD_1         1  ''
              108  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 42

    def test_streams_raises_valueerror--- This code section failed: ---

 L. 167         0  LOAD_GLOBAL              BTrDB
                2  LOAD_CONST               None
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'db'

 L. 168         8  LOAD_GLOBAL              pytest
               10  LOAD_METHOD              raises
               12  LOAD_GLOBAL              ValueError
               14  CALL_METHOD_1         1  ''
               16  SETUP_WITH           34  'to 34'
               18  STORE_FAST               'exc'

 L. 169        20  LOAD_FAST                'db'
               22  LOAD_METHOD              streams
               24  LOAD_CONST               11
               26  CALL_METHOD_1         1  ''
               28  POP_TOP          
               30  POP_BLOCK        
               32  BEGIN_FINALLY    
             34_0  COME_FROM_WITH       16  '16'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 32

    def test_info(self):
        """
        Assert info method returns a dict
        """
        serialized = b'\x18\x05*\x055.0.02\x10\n\x0elocalhost:4410'
        info = btrdb_pb2.InfoResponse.FromStringserialized
        endpoint = Mock(Endpoint)
        endpoint.info = Mock(return_value=info)
        conn = BTrDB(endpoint)
        truth = {'majorVersion':5, 
         'build':'5.0.0', 
         'proxy':{'proxyEndpoints': ['localhost:4410']}}
        info = conn.info()
        assert info == truth
        assert info['proxy']['proxyEndpoints'].__class__ == list

    def test_list_collections(self):
        """
        Assert list_collections method works
        """
        endpoint = Mock(Endpoint)
        endpoint.listCollections = Mock(side_effect=[
         iter([
          [
           'allen/automated'],
          [
           'allen/bindings']])])
        conn = BTrDB(endpoint)
        truth = [
         'allen/automated', 'allen/bindings']
        assert conn.list_collections() == truth

    @patch('btrdb.conn.unpack_stream_descriptor')
    def test_streams_in_collections_args(self, mock_util):
        """
        Assert streams_in_collections correctly sends *collection, tags, annotations
        to the endpoint method
        """
        descriptor = Mock()
        type(descriptor).uuid = PropertyMock(return_value=(uuidlib.uuid4().bytes))
        type(descriptor).collection = PropertyMock(return_value='fruit/apple')
        type(descriptor).propertyVersion = PropertyMock(return_value=22)
        mock_util.side_effect = [({'name': 'gala'}, {}), ({'name': 'fuji'}, {})]
        endpoint = Mock(Endpoint)
        endpoint.lookupStreams = Mock(side_effect=[[[descriptor]], [[descriptor]]])
        conn = BTrDB(endpoint)
        tags = {'unit': 'volts'}
        annotations = {'size': 'large'}
        streams = conn.streams_in_collection('a', 'b', is_collection_prefix=False, tags=tags,
          annotations=annotations)
        assert streams[0].name == 'gala'
        assert streams[1].name == 'fuji'
        expected = [
         call('a', False, tags, annotations), call('b', False, tags, annotations)]
        assert endpoint.lookupStreams.call_args_list == expected

    def test_streams_in_collections_no_arg(self):
        """
        Assert streams_in_collections calls lookupStreams if collections not sent
        """
        endpoint = Mock(Endpoint)
        endpoint.lookupStreams.return_value = []
        conn = BTrDB(endpoint)
        annotations = {'size': 'large'}
        streams = conn.streams_in_collection(annotations=annotations)
        assert endpoint.lookupStreams.called