# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/btrdb/test_stream.py
# Compiled at: 2020-05-13 17:11:01
# Size of source mod 2**32: 63199 bytes
__doc__ = '\nTesting package for the btrdb stream module\n'
import re, sys, json, uuid, pytz, pytest, datetime
from unittest.mock import Mock, PropertyMock, patch, call
from btrdb.conn import BTrDB
from btrdb.endpoint import Endpoint
from btrdb import MINIMUM_TIME, MAXIMUM_TIME
from btrdb.stream import Stream, StreamSet, StreamFilter, INSERT_BATCH_SIZE
from btrdb.point import RawPoint, StatPoint
from btrdb.exceptions import BTrDBError, InvalidOperation
from btrdb.grpcinterface import btrdb_pb2
RawPointProto = btrdb_pb2.RawPoint
StatPointProto = btrdb_pb2.StatPoint
EST = pytz.timezone('America/New_York')

@pytest.fixture
def stream1():
    uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
    stream = Mock(Stream)
    stream.version = Mock(return_value=11)
    stream.uuid = Mock(return_value=uu)
    stream.nearest = Mock(return_value=(RawPoint(time=10, value=1), 11))
    type(stream).collection = PropertyMock(return_value='fruits/apple')
    type(stream).name = PropertyMock(return_value='gala')
    stream.tags = Mock(return_value={'name':'gala',  'unit':'volts'})
    stream.annotations = Mock(return_value=({'owner':'ABC',  'color':'red'}, 11))
    return stream


@pytest.fixture
def stream2():
    uu = uuid.UUID('17dbe387-89ea-42b6-864b-f505cdb483f5')
    stream = Mock(Stream)
    stream.version = Mock(return_value=22)
    stream.uuid = Mock(return_value=uu)
    stream.nearest = Mock(return_value=(RawPoint(time=20, value=1), 22))
    type(stream).collection = PropertyMock(return_value='fruits/orange')
    type(stream).name = PropertyMock(return_value='blood')
    stream.tags = Mock(return_value={'name':'blood',  'unit':'amps'})
    stream.annotations = Mock(return_value=({'owner':'ABC',  'color':'orange'}, 22))
    return stream


class TestStream(object):

    def test_create(self):
        """
        Assert we can create the object
        """
        Stream(None, 'FAKE')

    def test_repr_str(self):
        """
        Assert the repr and str output are correct
        """
        COLLECTION = 'relay/foo'
        NAME = 'LINE222VA-ANG'
        stream = Stream(None, 'FAKE')
        stream._collection = COLLECTION
        stream._tags = {'name': NAME}
        expected = '<Stream collection={} name={}>'.format(COLLECTION, NAME)
        assert stream.__repr__() == expected
        assert stream.__str__() == expected

    def test_refresh_metadata(self):
        """
        Assert refresh_metadata calls Endpoint.streamInfo
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        stream.refresh_metadata()
        stream._btrdb.ep.streamInfo.assert_called_once_with(uu, False, True)

    def test_refresh_metadata_deserializes_annotations(self):
        """
        Assert refresh_metadata deserializes annotation values
        """
        uu = uuid.uuid4()
        serialized = {'acronym':'VPHM', 
         'description':'El Segundo PMU 42 Ean', 
         'devacronym':'PMU!EL_SEG_PMU_42', 
         'enabled':'true', 
         'id':'76932ae4-09bc-472c-8dc6-64fea68d2797', 
         'phase':'A', 
         'label':'null', 
         'frequency':'30', 
         'control':'2019-11-07 13:21:23.000000-0500', 
         'calibrate':'{"racf": 1.8, "pacf": 0.005}'}
        expected = {'acronym':'VPHM', 
         'description':'El Segundo PMU 42 Ean', 
         'devacronym':'PMU!EL_SEG_PMU_42', 
         'enabled':True, 
         'id':'76932ae4-09bc-472c-8dc6-64fea68d2797', 
         'phase':'A', 
         'label':None, 
         'frequency':30, 
         'control':'2019-11-07 13:21:23.000000-0500', 
         'calibrate':{'racf':1.8, 
          'pacf':0.005}}
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, serialized, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        stream.refresh_metadata()
        assert stream.annotations()[0] == expected

    def test_stream_name_property(self):
        """
        Assert name property comes from tags
        """
        name = 'LINE222VA-ANG'
        stream = Stream(None, 'FAKE_UUID')
        stream._tags = {'name': name}
        assert stream.name == name

    def test_stream_unit_property(self):
        """
        Assert unit property comes from tags
        """
        unit = 'whales'
        stream = Stream(None, 'FAKE_UUID')
        stream._tags = {'unit': unit}
        assert stream.unit == unit

    def test_update_arguments--- This code section failed: ---

 L. 181         0  LOAD_GLOBAL              uuid
                2  LOAD_METHOD              UUID
                4  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'uu'

 L. 182        10  LOAD_GLOBAL              Mock
               12  LOAD_GLOBAL              Endpoint
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'endpoint'

 L. 183        18  LOAD_GLOBAL              Stream
               20  LOAD_GLOBAL              BTrDB
               22  LOAD_FAST                'endpoint'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'uu'
               28  LOAD_CONST               ('btrdb', 'uuid')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  STORE_FAST               'stream'

 L. 186        34  LOAD_GLOBAL              pytest
               36  LOAD_METHOD              raises
               38  LOAD_GLOBAL              ValueError
               40  CALL_METHOD_1         1  ''
               42  SETUP_WITH           58  'to 58'
               44  STORE_FAST               'exc'

 L. 187        46  LOAD_FAST                'stream'
               48  LOAD_METHOD              update
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          
               54  POP_BLOCK        
               56  BEGIN_FINALLY    
             58_0  COME_FROM_WITH       42  '42'
               58  WITH_CLEANUP_START
               60  WITH_CLEANUP_FINISH
               62  END_FINALLY      

 L. 188        64  LOAD_STR                 'must supply'
               66  LOAD_GLOBAL              str
               68  LOAD_FAST                'exc'
               70  CALL_FUNCTION_1       1  ''
               72  COMPARE_OP               in
               74  POP_JUMP_IF_TRUE     80  'to 80'
               76  LOAD_ASSERT              AssertionError
               78  RAISE_VARARGS_1       1  ''
             80_0  COME_FROM            74  '74'

 L. 191        80  LOAD_GLOBAL              pytest
               82  LOAD_METHOD              raises
               84  LOAD_GLOBAL              TypeError
               86  CALL_METHOD_1         1  ''
               88  SETUP_WITH          108  'to 108'
               90  STORE_FAST               'exc'

 L. 192        92  LOAD_FAST                'stream'
               94  LOAD_ATTR                update
               96  BUILD_LIST_0          0 
               98  LOAD_CONST               ('tags',)
              100  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              102  POP_TOP          
              104  POP_BLOCK        
              106  BEGIN_FINALLY    
            108_0  COME_FROM_WITH       88  '88'
              108  WITH_CLEANUP_START
              110  WITH_CLEANUP_FINISH
              112  END_FINALLY      

 L. 193       114  LOAD_STR                 'tags must be of type dict'
              116  LOAD_GLOBAL              str
              118  LOAD_FAST                'exc'
              120  CALL_FUNCTION_1       1  ''
              122  COMPARE_OP               in
              124  POP_JUMP_IF_TRUE    130  'to 130'
              126  LOAD_ASSERT              AssertionError
              128  RAISE_VARARGS_1       1  ''
            130_0  COME_FROM           124  '124'

 L. 196       130  LOAD_GLOBAL              pytest
              132  LOAD_METHOD              raises
              134  LOAD_GLOBAL              TypeError
              136  CALL_METHOD_1         1  ''
              138  SETUP_WITH          158  'to 158'
              140  STORE_FAST               'exc'

 L. 197       142  LOAD_FAST                'stream'
              144  LOAD_ATTR                update
              146  BUILD_LIST_0          0 
              148  LOAD_CONST               ('annotations',)
              150  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              152  POP_TOP          
              154  POP_BLOCK        
              156  BEGIN_FINALLY    
            158_0  COME_FROM_WITH      138  '138'
              158  WITH_CLEANUP_START
              160  WITH_CLEANUP_FINISH
              162  END_FINALLY      

 L. 198       164  LOAD_STR                 'annotations must be of type dict'
              166  LOAD_GLOBAL              str
              168  LOAD_FAST                'exc'
              170  CALL_FUNCTION_1       1  ''
              172  COMPARE_OP               in
              174  POP_JUMP_IF_TRUE    180  'to 180'
              176  LOAD_ASSERT              AssertionError
              178  RAISE_VARARGS_1       1  ''
            180_0  COME_FROM           174  '174'

 L. 201       180  LOAD_GLOBAL              pytest
              182  LOAD_METHOD              raises
              184  LOAD_GLOBAL              TypeError
              186  CALL_METHOD_1         1  ''
              188  SETUP_WITH          208  'to 208'
              190  STORE_FAST               'exc'

 L. 202       192  LOAD_FAST                'stream'
              194  LOAD_ATTR                update
              196  LOAD_CONST               42
              198  LOAD_CONST               ('collection',)
              200  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              202  POP_TOP          
              204  POP_BLOCK        
              206  BEGIN_FINALLY    
            208_0  COME_FROM_WITH      188  '188'
              208  WITH_CLEANUP_START
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      

 L. 203       214  LOAD_STR                 'collection must be of type string'
              216  LOAD_GLOBAL              str
              218  LOAD_FAST                'exc'
              220  CALL_FUNCTION_1       1  ''
              222  COMPARE_OP               in
              224  POP_JUMP_IF_TRUE    230  'to 230'
              226  LOAD_ASSERT              AssertionError
              228  RAISE_VARARGS_1       1  ''
            230_0  COME_FROM           224  '224'

Parse error at or near `BEGIN_FINALLY' instruction at offset 56

    def test_update_tags(self):
        """
        Assert update calls correct Endpoint methods for tags update
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        tags = {'cat': 'dog'}
        stream.update(tags=tags)
        stream._btrdb.ep.setStreamTags.assert_called_once_with(uu=uu, expected=42, tags=tags,
          collection='koala')
        stream._btrdb.ep.setStreamAnnotations.assert_not_called()

    def test_update_collection(self):
        """
        Assert update calls correct Endpoint methods for collection update
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        collection = 'giraffe'
        stream.update(collection=collection)
        stream._btrdb.ep.setStreamTags.assert_called_once_with(uu=uu, expected=42, tags=(stream.tags()),
          collection=collection)
        stream._btrdb.ep.setStreamAnnotations.assert_not_called()

    def test_update_annotations(self):
        """
        Assert update calls correct Endpoint methods for annotations update
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        annotations = {'acronym':'VPHM', 
         'description':'El Segundo PMU 42 Ean', 
         'devacronym':'PMU!EL_SEG_PMU_42', 
         'enabled':True, 
         'id':uuid.UUID('76932ae4-09bc-472c-8dc6-64fea68d2797'), 
         'phase':'A', 
         'label':None, 
         'frequency':30, 
         'control':EST.localize(datetime.datetime(2019, 11, 7, 13, 21, 23)), 
         'calibrate':{'racf':1.8, 
          'pacf':0.005}}
        stream.refresh_metadata()
        stream.update(annotations=annotations)
        stream._btrdb.ep.setStreamAnnotations.assert_called_once_with(uu=uu,
          expected=42,
          changes={'acronym':'VPHM', 
         'description':'El Segundo PMU 42 Ean', 
         'devacronym':'PMU!EL_SEG_PMU_42', 
         'enabled':'true', 
         'id':'76932ae4-09bc-472c-8dc6-64fea68d2797', 
         'phase':'A', 
         'label':'null', 
         'frequency':'30', 
         'control':'2019-11-07 13:21:23.000000-0500', 
         'calibrate':'{"racf": 1.8, "pacf": 0.005}'},
          removals=[])
        stream._btrdb.ep.setStreamTags.assert_not_called()

    def test_update_annotations_nested_conversions(self):
        """
        Assert update correctly encodes nested annotation data
        """
        annotations = {'num':10, 
         'float':1.3, 
         'string':'the quick brown fox is 10', 
         'nested':{'num':11, 
          'float':1.3, 
          'string':'the quick brown fox is 11', 
          'nested':{'num':12, 
           'float':1.3, 
           'string':'the quick brown fox is 12'}}}
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {'foo': '42 Cherry Hill'}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        stream.refresh_metadata()
        stream.update(annotations=annotations)
        changes = stream._btrdb.ep.setStreamAnnotations.call_args[1]['changes']
        assert changes['nested'].__class__ == str
        assert json.loads(changes['nested']) == annotations['nested']
        if sys.version_info[0] > 3.5:
            stream._btrdb.ep.setStreamAnnotations.assert_called_once_with(uu=uu,
              expected=42,
              changes={'num':'10', 
             'float':'1.3', 
             'string':'"the quick brown fox is 10"', 
             'nested':'{"num": 11, "float": 1.3, "string": "the quick brown fox is 11", "nested": {"num": 12, "float": 1.3, "string": "the quick brown fox is 12"}}'})

    def test_update_annotations_no_encoder(self):
        """
        Assert update annotations works with None as encoder argument
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        annotations = {'foo':'this is a string', 
         'bar':'3.14'}
        stream.refresh_metadata()
        stream.update(annotations=annotations, encoder=None)
        stream._btrdb.ep.setStreamAnnotations.assert_called_once_with(uu=uu,
          expected=42,
          changes=annotations,
          removals=[])

    def test_update_annotations_replace(self):
        """
        Assert that replace argument will add proper keys to removals array in
        endpoint call.
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('koala', 42, {}, {'phase':'A',  'source':'PJM'}, None))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        annotations = {'foo':'this is a string', 
         'phase':'A'}
        stream.refresh_metadata()
        stream.update(annotations=annotations, replace=True)
        stream._btrdb.ep.setStreamAnnotations.assert_called_once_with(uu=uu,
          expected=42,
          changes=annotations,
          removals=[
         'source'])
        stream.update(annotations={}, replace=True)
        stream._btrdb.ep.setStreamAnnotations.assert_called_with(uu=uu,
          expected=42,
          changes={},
          removals=[
         'phase', 'source'])

    def test_exists_cached_value(self):
        """
        Assert exists first uses cached value
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, known_to_exist=True)
        stream.refresh_metadata = Mock()
        assert stream.exists()
        stream.refresh_metadata.assert_not_called()

    def test_exists(self):
        """
        Assert exists refreshes data if value is unknown
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu)
        stream.refresh_metadata = Mock(return_value=True)
        assert stream.exists()
        assert stream.refresh_metadata.call_count == 1

    def test_exists_returns_false_on_404(self):
        """
        Assert exists returns False on 404 error
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu)
        stream.refresh_metadata = Mock(side_effect=BTrDBError(code=404, msg='hello', mash=''))
        assert stream.exists() == False
        assert stream.refresh_metadata.call_count == 1

    def test_exists_passes_other_errors(self):
        """
        Assert exists does not keep non 404 errors trapped
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu)
        stream.refresh_metadata = Mock(side_effect=(ValueError()))
        with pytest.raises(ValueError):
            stream.exists()
        assert stream.refresh_metadata.call_count == 1

    def test_tags_returns_copy(self):
        """
        Assert tags returns a copy of the tags dict
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        token = {'cat': 'dog'}
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, tags=token)
        assert stream.tags() is not token
        assert stream.tags() == token

    def test_tags_returns_cached_values(self):
        """
        Assert tags returns a copy of the tags dict
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        token = {'cat': 'dog'}
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, tags=token, property_version=42)
        stream.refresh_metadata = Mock()
        assert stream.tags(refresh=False) == token
        stream.refresh_metadata.assert_not_called()

    def test_tags_forces_refresh_if_requested(self):
        """
        Assert tags calls refresh_metadata if requested even though a
        cached copy is available
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        token = {'cat': 'dog'}
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, tags=token)
        stream.refresh_metadata = Mock()
        stream.tags(refresh=True)
        assert stream.refresh_metadata.call_count == 1

    def test_annotations_returns_copy_of_value(self):
        """
        Assert annotations returns a copy of the annotations dict
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        token = {'cat': 'dog'}
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, annotations=token, property_version=42)
        stream.refresh_metadata = Mock()
        assert stream.annotations(refresh=False)[0] == token
        assert stream.annotations(refresh=False)[0] is not token
        assert stream.annotations(refresh=False)[1] == 42

    def test_annotations_returns_cached_values(self):
        """
        Assert annotations returns a copy of the annotations dict
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        token = {'cat': 'dog'}
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, annotations=token, property_version=42)
        stream.refresh_metadata = Mock()
        assert stream.annotations(refresh=False)[0] == token
        stream.refresh_metadata.assert_not_called()

    def test_annotations_forces_refresh_if_requested(self):
        """
        Assert annotations calls refresh_metadata if requested even though a
        cached copy is available
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        token = {'cat': 'dog'}
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu, annotations=token)
        stream.refresh_metadata = Mock()
        stream.annotations(refresh=True)
        assert stream.refresh_metadata.call_count == 1

    def test_windows(self):
        """
        Assert windows returns tuples of data from Endpoint.windows
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        windows = [
         [
          (
           StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6), StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7)), 42],
         [
          (
           StatPointProto(time=3, min=4, mean=5, max=6, count=7, stddev=8), StatPointProto(time=4, min=5, mean=6, max=7, count=8, stddev=9)), 42]]
        expected = (
         (
          StatPoint(time=1, minv=2.0, meanv=3.0, maxv=4.0, count=5, stddev=6.0), 42), (StatPoint(time=2, minv=3.0, meanv=4.0, maxv=5.0, count=6, stddev=7.0), 42),
         (
          StatPoint(time=3, minv=4.0, meanv=5.0, maxv=6.0, count=7, stddev=8.0), 42), (StatPoint(time=4, minv=5.0, meanv=6.0, maxv=7.0, count=8, stddev=9.0), 42))
        endpoint.windows = Mock(return_value=windows)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        params = {'start':100,  'end':500,  'width':2}
        result = (stream.windows)(**params)
        assert result == expected
        assert isinstance(result, tuple)
        assert isinstance(result[0], tuple)
        stream._btrdb.ep.windows.assert_called_once_with(uu, 100, 500, 2, 0, 0)

    def test_aligned_windows(self):
        """
        Assert windows returns tuples of data from Endpoint.alignedWindows
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        windows = [
         [
          (
           StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6), StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7)), 42],
         [
          (
           StatPointProto(time=3, min=4, mean=5, max=6, count=7, stddev=8), StatPointProto(time=4, min=5, mean=6, max=7, count=8, stddev=9)), 42]]
        expected = (
         (
          StatPoint(time=1, minv=2.0, meanv=3.0, maxv=4.0, count=5, stddev=6.0), 42), (StatPoint(time=2, minv=3.0, meanv=4.0, maxv=5.0, count=6, stddev=7.0), 42),
         (
          StatPoint(time=3, minv=4.0, meanv=5.0, maxv=6.0, count=7, stddev=8.0), 42), (StatPoint(time=4, minv=5.0, meanv=6.0, maxv=7.0, count=8, stddev=9.0), 42))
        endpoint.alignedWindows = Mock(return_value=windows)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        params = {'start':100,  'end':500,  'pointwidth':1}
        result = (stream.aligned_windows)(**params)
        assert result == expected
        assert isinstance(result, tuple)
        assert isinstance(result[0], tuple)
        stream._btrdb.ep.alignedWindows.assert_called_once_with(uu, 100, 500, 1, 0)

    def test_count(self):
        """
        Test that stream count method uses aligned windows
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        windows = [
         [
          (
           StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6), StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7)), 42],
         [
          (
           StatPointProto(time=3, min=4, mean=5, max=6, count=7, stddev=8), StatPointProto(time=4, min=5, mean=6, max=7, count=8, stddev=9)), 42]]
        endpoint.alignedWindows = Mock(return_value=windows)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        assert stream.count(precise=False, version=0) == 26
        stream._btrdb.ep.alignedWindows.assert_called_once_with(uu, MINIMUM_TIME, MAXIMUM_TIME, 60, 0)
        stream.count(10, 1000, 8, version=1200)
        stream._btrdb.ep.alignedWindows.assert_called_with(uu, 10, 1000, 8, 1200)

    def test_earliest(self):
        """
        Assert earliest calls Endpoint.nearest
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(return_value=(RawPointProto(time=100, value=1.0), 42))
        point, ver = stream.earliest()
        assert (point, ver) == (RawPoint(100, 1.0), 42)
        endpoint.nearest.assert_called_once_with(uu, MINIMUM_TIME, 0, False)

    def test_earliest_swallows_exception(self):
        """
        Assert earliest returns None when endpoint throws exception
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(side_effect=(BTrDBError(401, 'empty', None)))
        assert stream.earliest() is None
        endpoint.nearest.assert_called_once_with(uu, MINIMUM_TIME, 0, False)

    def test_earliest_passes_exception--- This code section failed: ---

 L. 640         0  LOAD_GLOBAL              uuid
                2  LOAD_METHOD              UUID
                4  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'uu'

 L. 641        10  LOAD_GLOBAL              Mock
               12  LOAD_GLOBAL              Endpoint
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'endpoint'

 L. 642        18  LOAD_GLOBAL              Stream
               20  LOAD_GLOBAL              BTrDB
               22  LOAD_FAST                'endpoint'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'uu'
               28  LOAD_CONST               ('btrdb', 'uuid')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  STORE_FAST               'stream'

 L. 643        34  LOAD_GLOBAL              Mock
               36  LOAD_GLOBAL              BTrDBError
               38  LOAD_CONST               999
               40  LOAD_STR                 'empty'
               42  LOAD_CONST               None
               44  CALL_FUNCTION_3       3  ''
               46  LOAD_CONST               ('side_effect',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  LOAD_FAST                'endpoint'
               52  STORE_ATTR               nearest

 L. 645        54  LOAD_GLOBAL              pytest
               56  LOAD_METHOD              raises
               58  LOAD_GLOBAL              BTrDBError
               60  CALL_METHOD_1         1  ''
               62  SETUP_WITH           78  'to 78'
               64  STORE_FAST               'exc'

 L. 646        66  LOAD_FAST                'stream'
               68  LOAD_METHOD              earliest
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_WITH       62  '62'
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      

 L. 647        84  LOAD_FAST                'exc'
               86  LOAD_ATTR                value
               88  LOAD_ATTR                code
               90  LOAD_CONST               999
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_TRUE    100  'to 100'
               96  LOAD_ASSERT              AssertionError
               98  RAISE_VARARGS_1       1  ''
            100_0  COME_FROM            94  '94'

 L. 648       100  LOAD_FAST                'endpoint'
              102  LOAD_ATTR                nearest
              104  LOAD_METHOD              assert_called_once_with
              106  LOAD_FAST                'uu'
              108  LOAD_GLOBAL              MINIMUM_TIME
              110  LOAD_CONST               0
              112  LOAD_CONST               False
              114  CALL_METHOD_4         4  ''
              116  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 76

    def test_latest(self):
        """
        Assert latest calls Endpoint.nearest
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(return_value=(RawPointProto(time=100, value=1.0), 42))
        point, ver = stream.latest()
        assert (
         point, ver) == (RawPoint(100, 1.0), 42)
        endpoint.nearest.assert_called_once_with(uu, MAXIMUM_TIME, 0, True)

    def test_latest_swallows_exception(self):
        """
        Assert latest returns None when endpoint throws exception
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(side_effect=(BTrDBError(401, 'empty', None)))
        assert stream.latest() is None
        endpoint.nearest.assert_called_once_with(uu, MAXIMUM_TIME, 0, True)

    def test_latest_passes_exception--- This code section failed: ---

 L. 682         0  LOAD_GLOBAL              uuid
                2  LOAD_METHOD              UUID
                4  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'uu'

 L. 683        10  LOAD_GLOBAL              Mock
               12  LOAD_GLOBAL              Endpoint
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'endpoint'

 L. 684        18  LOAD_GLOBAL              Stream
               20  LOAD_GLOBAL              BTrDB
               22  LOAD_FAST                'endpoint'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'uu'
               28  LOAD_CONST               ('btrdb', 'uuid')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  STORE_FAST               'stream'

 L. 685        34  LOAD_GLOBAL              Mock
               36  LOAD_GLOBAL              BTrDBError
               38  LOAD_CONST               999
               40  LOAD_STR                 'empty'
               42  LOAD_CONST               None
               44  CALL_FUNCTION_3       3  ''
               46  LOAD_CONST               ('side_effect',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  LOAD_FAST                'endpoint'
               52  STORE_ATTR               nearest

 L. 687        54  LOAD_GLOBAL              pytest
               56  LOAD_METHOD              raises
               58  LOAD_GLOBAL              BTrDBError
               60  CALL_METHOD_1         1  ''
               62  SETUP_WITH           78  'to 78'
               64  STORE_FAST               'exc'

 L. 688        66  LOAD_FAST                'stream'
               68  LOAD_METHOD              latest
               70  CALL_METHOD_0         0  ''
               72  POP_TOP          
               74  POP_BLOCK        
               76  BEGIN_FINALLY    
             78_0  COME_FROM_WITH       62  '62'
               78  WITH_CLEANUP_START
               80  WITH_CLEANUP_FINISH
               82  END_FINALLY      

 L. 689        84  LOAD_FAST                'exc'
               86  LOAD_ATTR                value
               88  LOAD_ATTR                code
               90  LOAD_CONST               999
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_TRUE    100  'to 100'
               96  LOAD_ASSERT              AssertionError
               98  RAISE_VARARGS_1       1  ''
            100_0  COME_FROM            94  '94'

 L. 690       100  LOAD_FAST                'endpoint'
              102  LOAD_ATTR                nearest
              104  LOAD_METHOD              assert_called_once_with
              106  LOAD_FAST                'uu'
              108  LOAD_GLOBAL              MAXIMUM_TIME
              110  LOAD_CONST               0
              112  LOAD_CONST               True
              114  CALL_METHOD_4         4  ''
              116  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 76

    @patch('btrdb.stream.currently_as_ns')
    def test_currently(self, mocked):
        """
        Assert currently calls Endpoint.nearest
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(return_value=(RawPointProto(time=100, value=1.0), 42))
        ns_fake_time = 1514808000000000000
        mocked.return_value = ns_fake_time
        point, ver = stream.current()
        assert (
         point, ver) == (RawPoint(100, 1.0), 42)
        endpoint.nearest.assert_called_once_with(uu, ns_fake_time, 0, True)

    @patch('btrdb.stream.currently_as_ns')
    def test_currently_swallows_exception(self, mocked):
        """
        Assert currently returns None when endpoint throws exception
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(side_effect=(BTrDBError(401, 'empty', None)))
        ns_fake_time = 1514808000000000000
        mocked.return_value = ns_fake_time
        assert stream.current() is None
        endpoint.nearest.assert_called_once_with(uu, ns_fake_time, 0, True)

    @patch('btrdb.stream.currently_as_ns')
    def test_currently_passes_exception--- This code section failed: ---

 L. 731         0  LOAD_GLOBAL              uuid
                2  LOAD_METHOD              UUID
                4  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'uu'

 L. 732        10  LOAD_GLOBAL              Mock
               12  LOAD_GLOBAL              Endpoint
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'endpoint'

 L. 733        18  LOAD_GLOBAL              Stream
               20  LOAD_GLOBAL              BTrDB
               22  LOAD_FAST                'endpoint'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'uu'
               28  LOAD_CONST               ('btrdb', 'uuid')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  STORE_FAST               'stream'

 L. 734        34  LOAD_GLOBAL              Mock
               36  LOAD_GLOBAL              BTrDBError
               38  LOAD_CONST               999
               40  LOAD_STR                 'empty'
               42  LOAD_CONST               None
               44  CALL_FUNCTION_3       3  ''
               46  LOAD_CONST               ('side_effect',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  LOAD_FAST                'endpoint'
               52  STORE_ATTR               nearest

 L. 735        54  LOAD_CONST               1514808000000000000
               56  STORE_FAST               'ns_fake_time'

 L. 736        58  LOAD_FAST                'ns_fake_time'
               60  LOAD_FAST                'mocked'
               62  STORE_ATTR               return_value

 L. 738        64  LOAD_GLOBAL              pytest
               66  LOAD_METHOD              raises
               68  LOAD_GLOBAL              BTrDBError
               70  CALL_METHOD_1         1  ''
               72  SETUP_WITH           88  'to 88'
               74  STORE_FAST               'exc'

 L. 739        76  LOAD_FAST                'stream'
               78  LOAD_METHOD              current
               80  CALL_METHOD_0         0  ''
               82  POP_TOP          
               84  POP_BLOCK        
               86  BEGIN_FINALLY    
             88_0  COME_FROM_WITH       72  '72'
               88  WITH_CLEANUP_START
               90  WITH_CLEANUP_FINISH
               92  END_FINALLY      

 L. 740        94  LOAD_FAST                'exc'
               96  LOAD_ATTR                value
               98  LOAD_ATTR                code
              100  LOAD_CONST               999
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_TRUE    110  'to 110'
              106  LOAD_ASSERT              AssertionError
              108  RAISE_VARARGS_1       1  ''
            110_0  COME_FROM           104  '104'

 L. 741       110  LOAD_FAST                'endpoint'
              112  LOAD_ATTR                nearest
              114  LOAD_METHOD              assert_called_once_with
              116  LOAD_FAST                'uu'
              118  LOAD_FAST                'ns_fake_time'
              120  LOAD_CONST               0
              122  LOAD_CONST               True
              124  CALL_METHOD_4         4  ''
              126  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 86

    def test_version(self):
        """
        Assert version calls and returns correct value from streamInfo
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.streamInfo = Mock(return_value=('', 0, {}, {}, 42))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        assert stream.version() == 42
        stream._btrdb.ep.streamInfo.assert_called_once_with(uu, True, False)

    def test_insert(self):
        """
        Assert insert batches data to endpoint insert and returns version
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.insert = Mock(side_effect=[1, 2, 3])
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        data = list(zip(range(10000, 120000), map(float, range(110000))))
        version = stream.insert(data)
        assert stream._btrdb.ep.insert.call_args_list[0][0][1] == data[:INSERT_BATCH_SIZE]
        assert stream._btrdb.ep.insert.call_args_list[1][0][1] == data[INSERT_BATCH_SIZE:2 * INSERT_BATCH_SIZE]
        assert stream._btrdb.ep.insert.call_args_list[2][0][1] == data[2 * INSERT_BATCH_SIZE:]
        assert version == 3

    def test_nearest(self):
        """
        Assert nearest calls Endpoint.nearest with correct arguments
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.nearest = Mock(return_value=(RawPointProto(time=100, value=1.0), 42))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        point, version = stream.nearest(5, 10, False)
        stream._btrdb.ep.nearest.assert_called_once_with(uu, 5, 10, False)
        assert point == RawPoint(100, 1.0)
        assert version == 42

    def test_nearest_swallows_exception(self):
        """
        Assert nearest returns None when endpoint throws 401 exception
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        endpoint.nearest = Mock(side_effect=(BTrDBError(401, 'empty', None)))
        assert stream.nearest(0, 0, False) is None
        endpoint.nearest.assert_called_once_with(uu, 0, 0, False)

    def test_nearest_passes_exception--- This code section failed: ---

 L. 811         0  LOAD_GLOBAL              uuid
                2  LOAD_METHOD              UUID
                4  LOAD_STR                 '0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'uu'

 L. 812        10  LOAD_GLOBAL              Mock
               12  LOAD_GLOBAL              Endpoint
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'endpoint'

 L. 813        18  LOAD_GLOBAL              Stream
               20  LOAD_GLOBAL              BTrDB
               22  LOAD_FAST                'endpoint'
               24  CALL_FUNCTION_1       1  ''
               26  LOAD_FAST                'uu'
               28  LOAD_CONST               ('btrdb', 'uuid')
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  STORE_FAST               'stream'

 L. 814        34  LOAD_GLOBAL              Mock
               36  LOAD_GLOBAL              BTrDBError
               38  LOAD_CONST               999
               40  LOAD_STR                 'empty'
               42  LOAD_CONST               None
               44  CALL_FUNCTION_3       3  ''
               46  LOAD_CONST               ('side_effect',)
               48  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               50  LOAD_FAST                'endpoint'
               52  STORE_ATTR               nearest

 L. 816        54  LOAD_GLOBAL              pytest
               56  LOAD_METHOD              raises
               58  LOAD_GLOBAL              BTrDBError
               60  CALL_METHOD_1         1  ''
               62  SETUP_WITH           84  'to 84'
               64  STORE_FAST               'exc'

 L. 817        66  LOAD_FAST                'stream'
               68  LOAD_METHOD              nearest
               70  LOAD_CONST               0
               72  LOAD_CONST               0
               74  LOAD_CONST               False
               76  CALL_METHOD_3         3  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       62  '62'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

 L. 818        90  LOAD_FAST                'exc'
               92  LOAD_ATTR                value
               94  LOAD_ATTR                code
               96  LOAD_CONST               999
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    106  'to 106'
              102  LOAD_ASSERT              AssertionError
              104  RAISE_VARARGS_1       1  ''
            106_0  COME_FROM           100  '100'

 L. 819       106  LOAD_FAST                'endpoint'
              108  LOAD_ATTR                nearest
              110  LOAD_METHOD              assert_called_once_with
              112  LOAD_FAST                'uu'
              114  LOAD_CONST               0
              116  LOAD_CONST               0
              118  LOAD_CONST               False
              120  CALL_METHOD_4         4  ''
              122  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 82

    def test_delete_range(self):
        """
        Assert delete_range calls Endpoint.deleteRange with correct arguments
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu)
        stream.delete(5, 10)
        stream._btrdb.ep.deleteRange.assert_called_once_with(uu, 5, 10)

    def test_flush(self):
        """
        Assert flush calls Endpoint.flush with UUID
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu)
        stream.flush()
        stream._btrdb.ep.flush.assert_called_once_with(uu)

    def test_obliterate(self):
        """
        Assert obliterate calls Endpoint.obliterate with UUID
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        stream = Stream(btrdb=(BTrDB(Mock(Endpoint))), uuid=uu)
        stream.obliterate()
        stream._btrdb.ep.obliterate.assert_called_once_with(uu)

    def test_obliterate_allows_error(self):
        """
        Assert obliterate raises error if stream not found. (does not swallow error)
        """
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        endpoint = Mock(Endpoint)
        endpoint.obliterate = Mock(side_effect=BTrDBError(code=404, msg='hello', mash=''))
        stream = Stream(btrdb=(BTrDB(endpoint)), uuid=uu)
        with pytest.raises(BTrDBError):
            stream.obliterate()
        stream._btrdb.ep.obliterate.assert_called_once_with(uu)


class TestStreamSet(object):

    def test_create(self):
        """
        Assert we can create the object
        """
        StreamSet([])

    def test_repr(self):
        """
        Assert StreamSet instance repr output
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        expected = '<StreamSet(4 streams)>'
        assert streams.__repr__() == expected
        data = [
         1]
        streams = StreamSet(data)
        expected = '<StreamSet(1 stream)>'
        assert streams.__repr__() == expected

    def test_str(self):
        """
        Assert StreamSet instance str output
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        expected = 'StreamSet with 4 streams'
        assert str(streams) == expected
        data = [
         1]
        streams = StreamSet(data)
        expected = 'StreamSet with 1 stream'
        assert str(streams) == expected

    def test_subscriptable(self):
        """
        Assert StreamSet instance is subscriptable
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        for index, val in enumerate(data):
            assert streams[index] == val

    def test_len(self):
        """
        Assert StreamSet instance support len
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        assert len(streams) == len(data)

    def test_iter(self):
        """
        Assert StreamSet instance support iteration
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        for index, stream in enumerate(streams):
            assert data[index] == stream

    def test_indexing(self):
        """
        Assert StreamSet instance supports indexing
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        assert streams[(-1)] == data[(-1)]
        for idx in range(len(streams)):
            assert data[idx] == streams[idx]
            assert streams[:2] == data[:2]

    def test_mapping--- This code section failed: ---

 L. 967         0  LOAD_LISTCOMP            '<code_object <listcomp>>'
                2  LOAD_STR                 'TestStreamSet.test_mapping.<locals>.<listcomp>'
                4  MAKE_FUNCTION_0          ''
                6  LOAD_GLOBAL              range
                8  LOAD_CONST               4
               10  CALL_FUNCTION_1       1  ''
               12  GET_ITER         
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'uuids'

 L. 968        18  LOAD_LISTCOMP            '<code_object <listcomp>>'
               20  LOAD_STR                 'TestStreamSet.test_mapping.<locals>.<listcomp>'
               22  MAKE_FUNCTION_0          ''
               24  LOAD_FAST                'uuids'
               26  GET_ITER         
               28  CALL_FUNCTION_1       1  ''
               30  STORE_FAST               'data'

 L. 969        32  LOAD_GLOBAL              StreamSet
               34  LOAD_FAST                'data'
               36  CALL_FUNCTION_1       1  ''
               38  STORE_FAST               'streams'

 L. 972        40  LOAD_FAST                'uuids'
               42  GET_ITER         
             44_0  COME_FROM            60  '60'
               44  FOR_ITER             68  'to 68'
               46  STORE_FAST               'uu'

 L. 973        48  LOAD_FAST                'streams'
               50  LOAD_FAST                'uu'
               52  BINARY_SUBSCR    
               54  LOAD_ATTR                uuid
               56  LOAD_FAST                'uu'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_TRUE     44  'to 44'
               62  LOAD_GLOBAL              AssertionError
               64  RAISE_VARARGS_1       1  ''
               66  JUMP_BACK            44  'to 44'

 L. 976        68  LOAD_FAST                'uuids'
               70  GET_ITER         
             72_0  COME_FROM            92  '92'
               72  FOR_ITER            100  'to 100'
               74  STORE_FAST               'uu'

 L. 977        76  LOAD_FAST                'streams'
               78  LOAD_GLOBAL              str
               80  LOAD_FAST                'uu'
               82  CALL_FUNCTION_1       1  ''
               84  BINARY_SUBSCR    
               86  LOAD_ATTR                uuid
               88  LOAD_FAST                'uu'
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_TRUE     72  'to 72'
               94  LOAD_GLOBAL              AssertionError
               96  RAISE_VARARGS_1       1  ''
               98  JUMP_BACK            72  'to 72'

 L. 980       100  LOAD_GLOBAL              uuid
              102  LOAD_METHOD              uuid4
              104  CALL_METHOD_0         0  ''
              106  STORE_FAST               'missing'

 L. 981       108  LOAD_GLOBAL              pytest
              110  LOAD_METHOD              raises
              112  LOAD_GLOBAL              KeyError
              114  CALL_METHOD_1         1  ''
              116  SETUP_WITH          132  'to 132'
              118  STORE_FAST               'e'

 L. 982       120  LOAD_FAST                'streams'
              122  LOAD_FAST                'missing'
              124  BINARY_SUBSCR    
              126  POP_TOP          
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM_WITH      116  '116'
              132  WITH_CLEANUP_START
              134  WITH_CLEANUP_FINISH
              136  END_FINALLY      

 L. 983       138  LOAD_GLOBAL              str
              140  LOAD_FAST                'missing'
              142  CALL_FUNCTION_1       1  ''
              144  LOAD_GLOBAL              str
              146  LOAD_FAST                'e'
              148  CALL_FUNCTION_1       1  ''
              150  COMPARE_OP               in
              152  POP_JUMP_IF_TRUE    158  'to 158'
              154  LOAD_ASSERT              AssertionError
              156  RAISE_VARARGS_1       1  ''
            158_0  COME_FROM           152  '152'

Parse error at or near `BEGIN_FINALLY' instruction at offset 130

    def test_contains(self):
        """
        Assert StreamSet instance supports contains
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        assert 'dog' in streams

    def test_reverse(self):
        """
        Assert StreamSet instance supports reversal
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        assert list(reversed(streams)) == list(reversed(data))

    def test_to_list(self):
        """
        Assert StreamSet instance cast to list
        """
        data = [
         11, 22, 'dog', 'cat']
        streams = StreamSet(data)
        assert list(streams) == data

    def test_allow_window(self):
        """
        Assert allow_window returns False if window already requested
        """
        streams = StreamSet([1, 2, 3])
        assert streams.allow_window == True
        streams.windows(30, 4)
        assert streams.allow_window == False
        streams = StreamSet([1, 2, 3])
        streams.aligned_windows(30)
        assert streams.allow_window == False

    def test_latest_versions(self, stream1, stream2):
        """
        Assert _latest_versions returns correct values
        """
        streams = StreamSet([stream1, stream2])
        expected = {stream1.uuid: stream1.version(), 
         stream2.uuid: stream2.version()}
        assert streams._latest_versions() == expected

    def test_pin_versions_returns_self(self, stream1):
        """
        Assert pin_versions returns self
        """
        streams = StreamSet([stream1])
        expected = {stream1.uuid(): stream1.version()}
        result = streams.pin_versions(expected)
        assert streams is result

    def test_pin_versions_with_argument(self):
        """
        Assert pin_versions uses supplied version numbers
        """
        streams = StreamSet([1, 2])
        expected = [3, 4]
        assert streams.pin_versions(expected) == streams
        assert streams._pinned_versions == expected

    def test_pin_versions_with_argument(self):
        """
        Assert pin_versions uses supplied version numbers
        """
        streams = StreamSet([1, 2])
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        expected = {uu: 42}
        assert streams.pin_versions(expected) == streams
        assert streams._pinned_versions == expected

    def test_pin_versions_no_argument(self, stream1, stream2):
        """
        Assert pin_versions uses latest version numbers
        """
        streams = StreamSet([stream1, stream2])
        uu = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        expected = {uu: 42}
        assert streams.pin_versions(expected) == streams
        assert streams._pinned_versions == expected

    def test_pin_versions_raise_on_non_dict--- This code section failed: ---

 L.1106         0  LOAD_GLOBAL              StreamSet
                2  LOAD_CONST               1
                4  BUILD_LIST_1          1 
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'streams'

 L.1107        10  LOAD_STR                 'INVALID DATA'
               12  STORE_FAST               'expected'

 L.1109        14  LOAD_GLOBAL              pytest
               16  LOAD_METHOD              raises
               18  LOAD_GLOBAL              TypeError
               20  CALL_METHOD_1         1  ''
               22  SETUP_WITH           44  'to 44'
               24  STORE_FAST               'e'

 L.1110        26  LOAD_FAST                'streams'
               28  LOAD_METHOD              pin_versions
               30  LOAD_FAST                'expected'
               32  CALL_METHOD_1         1  ''
               34  LOAD_FAST                'streams'
               36  COMPARE_OP               ==
               38  POP_TOP          
               40  POP_BLOCK        
               42  BEGIN_FINALLY    
             44_0  COME_FROM_WITH       22  '22'
               44  WITH_CLEANUP_START
               46  WITH_CLEANUP_FINISH
               48  END_FINALLY      

 L.1111        50  LOAD_STR                 'dict'
               52  LOAD_GLOBAL              str
               54  LOAD_FAST                'e'
               56  CALL_FUNCTION_1       1  ''
               58  LOAD_METHOD              lower
               60  CALL_METHOD_0         0  ''
               62  COMPARE_OP               in
               64  POP_JUMP_IF_TRUE     70  'to 70'
               66  LOAD_ASSERT              AssertionError
               68  RAISE_VARARGS_1       1  ''
             70_0  COME_FROM            64  '64'

Parse error at or near `BEGIN_FINALLY' instruction at offset 42

    def test_pin_versions_raise_on_non_uuid_key--- This code section failed: ---

 L.1119         0  LOAD_GLOBAL              StreamSet
                2  LOAD_CONST               1
                4  BUILD_LIST_1          1 
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'streams'

 L.1120        10  LOAD_STR                 'uuid'
               12  LOAD_CONST               42
               14  BUILD_MAP_1           1 
               16  STORE_FAST               'expected'

 L.1122        18  LOAD_GLOBAL              pytest
               20  LOAD_METHOD              raises
               22  LOAD_GLOBAL              TypeError
               24  CALL_METHOD_1         1  ''
               26  SETUP_WITH           48  'to 48'
               28  STORE_FAST               'e'

 L.1123        30  LOAD_FAST                'streams'
               32  LOAD_METHOD              pin_versions
               34  LOAD_FAST                'expected'
               36  CALL_METHOD_1         1  ''
               38  LOAD_FAST                'streams'
               40  COMPARE_OP               ==
               42  POP_TOP          
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_WITH       26  '26'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

 L.1124        54  LOAD_STR                 'uuid'
               56  LOAD_GLOBAL              str
               58  LOAD_FAST                'e'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_METHOD              lower
               64  CALL_METHOD_0         0  ''
               66  COMPARE_OP               in
               68  POP_JUMP_IF_TRUE     74  'to 74'
               70  LOAD_ASSERT              AssertionError
               72  RAISE_VARARGS_1       1  ''
             74_0  COME_FROM            68  '68'

Parse error at or near `BEGIN_FINALLY' instruction at offset 46

    def test_versions_no_pin(self, stream1, stream2):
        """
        Assert versions returns correctly if pin_versions not called
        """
        streams = StreamSet([stream1, stream2])
        expected = {stream1.uuid: stream1.version(), 
         stream2.uuid: stream2.version()}
        assert streams.versions() == expected

    def test_versions_with_pin(self, stream1, stream2):
        """
        Assert versions returns correctly if pin_versions called
        """
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        s1 = Mock(Stream)
        s1.version = Mock(return_value=11)
        s1.uuid = Mock(return_value=uu1)
        uu2 = uuid.UUID('17dbe387-89ea-42b6-864b-f505cdb483f5')
        s2 = Mock(Stream)
        s2.version = Mock(return_value=22)
        s2.uuid = Mock(return_value=uu2)
        streams = StreamSet([stream1, stream2])
        expected = {stream1.uuid(): 88, 
         stream2.uuid(): 99}
        streams.pin_versions(expected)
        assert streams.versions() == expected

    def test_earliest(self, stream1, stream2):
        """
        Assert earliest returns correct time code
        """
        streams = StreamSet([stream1, stream2])
        assert streams.latest() == (RawPoint(time=10, value=1), RawPoint(time=20, value=1))

    def test_latest(self, stream1, stream2):
        """
        Assert latest returns correct time code
        """
        streams = StreamSet([stream1, stream2])
        assert streams.latest() == (RawPoint(time=10, value=1), RawPoint(time=20, value=1))

    @patch('btrdb.stream.currently_as_ns')
    def test_current(self, mocked, stream1, stream2):
        """
        Assert current calls nearest with the current time
        """
        mocked.return_value = 15
        streams = StreamSet([stream1, stream2])
        streams.current()
        stream1.nearest.assert_called_once_with(15, version=11, backward=True)
        stream2.nearest.assert_called_once_with(15, version=22, backward=True)

    @patch('btrdb.stream.currently_as_ns')
    def test_currently_out_of_range(self, mocked):
        """
        Assert currently raises an exception if it is not filtered
        """
        mocked.return_value = 15
        streams = StreamSet([stream1, stream2])
        with pytest.raises(ValueError, match='current time is not included in filtered stream range'):
            streams.filter(start=20, end=30).current()
        with pytest.raises(ValueError, match='current time is not included in filtered stream range'):
            streams.filter(start=0, end=10).current()

    def test_count(self):
        """
        Test the stream set count method
        """
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        uu2 = uuid.UUID('4dadf38d-52a5-4b7a-ada9-a5d563f9538c')
        endpoint = Mock(Endpoint)
        windows = [
         [
          (
           StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6), StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7)), 42],
         [
          (
           StatPointProto(time=3, min=4, mean=5, max=6, count=7, stddev=8), StatPointProto(time=4, min=5, mean=6, max=7, count=8, stddev=9)), 42]]
        endpoint.alignedWindows = Mock(return_value=windows)
        streams = StreamSet([
         Stream(btrdb=(BTrDB(endpoint)), uuid=uu1),
         Stream(btrdb=(BTrDB(endpoint)), uuid=uu2)])
        assert streams.count() == 52
        endpoint.alignedWindows.assert_any_call(uu1, MINIMUM_TIME, MAXIMUM_TIME, 60, 0)
        endpoint.alignedWindows.assert_any_call(uu2, MINIMUM_TIME, MAXIMUM_TIME, 60, 0)

    def test_count_filtered(self):
        """
        Test the stream set count method with filters
        """
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        uu2 = uuid.UUID('4dadf38d-52a5-4b7a-ada9-a5d563f9538c')
        endpoint = Mock(Endpoint)
        endpoint.alignedWindows = Mock(return_value=[])
        streams = StreamSet([
         Stream(btrdb=(BTrDB(endpoint)), uuid=uu1),
         Stream(btrdb=(BTrDB(endpoint)), uuid=uu2)])
        windows = [
         [
          (
           StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6), StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7)), 42],
         [
          (
           StatPointProto(time=3, min=4, mean=5, max=6, count=7, stddev=8), StatPointProto(time=4, min=5, mean=6, max=7, count=8, stddev=9)), 42]]
        endpoint.alignedWindows = Mock(return_value=windows)
        streams = streams.filter(start=10, end=1000)
        streams.pin_versions({uu1: 42, uu2: 99})
        streams.count()
        endpoint.alignedWindows.assert_any_call(uu1, 10, 1000, 8, 42)
        endpoint.alignedWindows.assert_any_call(uu2, 10, 1000, 8, 99)

    def test_filter(self, stream1):
        """
        Assert filter creates and stores a StreamFilter object
        """
        streams = StreamSet([stream1])
        start, end = (1, 100)
        streams = streams.filter(start=start, end=end)
        assert len(streams.filters) == 1
        assert streams.filters[0].start == start
        assert streams.filters[0].end == end
        assert isinstance(streams.filters[0], StreamFilter)

    def test_filter_returns_new_instance(self, stream1):
        """
        Assert filter returns new instance
        """
        streams = StreamSet([stream1])
        start, end = (1, 100)
        other = streams.filter(start=start, end=end)
        assert other is not streams
        assert isinstance(other, streams.__class__)

    def test_filter_collection(self, stream1, stream2):
        """
        Assert filter collection works as intended
        """
        streams = StreamSet([stream1, stream2])
        other = streams.filter(collection='fruits')
        assert other._streams == []
        other = streams.filter(collection='fruits/apple')
        assert other._streams == [stream1]
        other = streams.filter(collection='FRUITS/APPLE')
        assert other._streams == [stream1]
        other = streams.filter(collection='fruits*')
        assert other._streams == []
        other = streams.filter(collection=(re.compile('fruits')))
        assert other._streams == [stream1, stream2]
        other = streams.filter(collection=(re.compile('fruits.*')))
        assert other._streams == [stream1, stream2]
        type(stream1).collection = PropertyMock(return_value='foo/region-north')
        other = streams.filter(collection=(re.compile('region-')))
        assert other._streams == [stream1]
        other = streams.filter(collection=(re.compile('^region-')))
        assert other._streams == []
        other = streams.filter(collection=(re.compile('foo/')))
        assert other._streams == [stream1]
        other = streams.filter(collection=(re.compile('foo/z')))
        assert other._streams == []
        type(stream1).collection = PropertyMock(return_value='region.north/foo')
        other = streams.filter(collection=(re.compile('region\\.')))
        assert other._streams == [stream1]

    def test_filter_name(self, stream1, stream2):
        """
        Assert filter name works as intended
        """
        streams = StreamSet([stream1, stream2])
        other = streams.filter(name='blood')
        assert other._streams == [stream2]
        other = streams.filter(name='BLOOD')
        assert other._streams == [stream2]
        other = streams.filter(name='not_found')
        assert other._streams == []
        other = streams.filter(name=(re.compile('blood')))
        assert other._streams == [stream2]
        other = streams.filter(name=(re.compile('^blood$')))
        assert other._streams == [stream2]
        other = streams.filter(name=(re.compile('oo')))
        assert other._streams == [stream2]
        other = streams.filter(name=(re.compile('not_found')))
        assert other._streams == []
        type(stream1).name = PropertyMock(return_value='region-north')
        other = streams.filter(name=(re.compile('region-')))
        assert other._streams == [stream1]
        other = streams.filter(name=(re.compile('region\\.')))
        assert other._streams == []
        type(stream1).name = PropertyMock(return_value='region.north')
        other = streams.filter(name=(re.compile('region\\.')))
        assert other._streams == [stream1]

    def test_filter_unit(self, stream1, stream2):
        """
        Assert filter unit works as intended
        """
        streams = StreamSet([stream1, stream2])
        other = streams.filter(unit='volts')
        assert other._streams == [stream1]
        other = streams.filter(unit='VOLTS')
        assert other._streams == [stream1]
        other = streams.filter(unit='not_found')
        assert other._streams == []
        other = streams.filter(unit=(re.compile('volts|amps')))
        assert other._streams == [stream1, stream2]
        other = streams.filter(unit=(re.compile('volts')))
        assert other._streams == [stream1]
        other = streams.filter(unit=(re.compile('v')))
        assert other._streams == [stream1]
        other = streams.filter(unit=(re.compile('meters')))
        assert other._streams == []

    def test_filter_tags(self, stream1, stream2):
        """
        Assert filter annotations works as intended
        """
        streams = StreamSet([stream1, stream2])
        other = streams.filter(tags={'unit': 'meters'})
        assert other._streams == []
        other = streams.filter(tags={'unit': 'volts'})
        assert other._streams == [stream1]
        stream2.tags.return_value = {'name':'blood', 
         'unit':'volts'}
        other = streams.filter(tags={'name':'blood',  'unit':'volts'})
        assert other._streams == [stream2]
        other = streams.filter(tags={'unit': 'volts'})
        assert other._streams == [stream1, stream2]

    def test_filter_annotations(self, stream1, stream2):
        """
        Assert filter annotations works as intended
        """
        streams = StreamSet([stream1, stream2])
        other = streams.filter(annotations={'owner': ''})
        assert other._streams == []
        other = streams.filter(annotations={'owner': 'ABC'})
        assert other._streams == [stream1, stream2]
        other = streams.filter(annotations={'color': 'red'})
        assert other._streams == [stream1]
        other = streams.filter(annotations={'owner':'ABC',  'color':'red'})
        assert other._streams == [stream1]

    def test_clone_returns_new_object(self, stream1, stream2):
        """
        Assert that clone returns a different object
        """
        streams = StreamSet([stream1, stream2])
        clone = streams.clone()
        assert id(clone) != id(streams)
        assert clone._streams is streams._streams

    def test_windows_raises_valueerror--- This code section failed: ---

 L.1448         0  LOAD_GLOBAL              StreamSet
                2  LOAD_FAST                'stream1'
                4  BUILD_LIST_1          1 
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'streams'

 L.1449        10  LOAD_GLOBAL              pytest
               12  LOAD_METHOD              raises
               14  LOAD_GLOBAL              ValueError
               16  CALL_METHOD_1         1  ''
               18  SETUP_WITH           38  'to 38'
               20  STORE_FAST               'exc'

 L.1450        22  LOAD_FAST                'streams'
               24  LOAD_METHOD              windows
               26  LOAD_STR                 'invalid'
               28  LOAD_CONST               42
               30  CALL_METHOD_2         2  ''
               32  POP_TOP          
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_WITH       18  '18'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L.1451        44  LOAD_STR                 'literal'
               46  LOAD_GLOBAL              str
               48  LOAD_FAST                'exc'
               50  CALL_FUNCTION_1       1  ''
               52  LOAD_METHOD              lower
               54  CALL_METHOD_0         0  ''
               56  COMPARE_OP               in
               58  POP_JUMP_IF_TRUE     64  'to 64'
               60  LOAD_ASSERT              AssertionError
               62  RAISE_VARARGS_1       1  ''
             64_0  COME_FROM            58  '58'

 L.1453        64  LOAD_GLOBAL              pytest
               66  LOAD_METHOD              raises
               68  LOAD_GLOBAL              ValueError
               70  CALL_METHOD_1         1  ''
               72  SETUP_WITH           92  'to 92'
               74  STORE_FAST               'exc'

 L.1454        76  LOAD_FAST                'streams'
               78  LOAD_METHOD              windows
               80  LOAD_CONST               42
               82  LOAD_STR                 'invalid'
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH       72  '72'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

 L.1455        98  LOAD_STR                 'literal'
              100  LOAD_GLOBAL              str
              102  LOAD_FAST                'exc'
              104  CALL_FUNCTION_1       1  ''
              106  LOAD_METHOD              lower
              108  CALL_METHOD_0         0  ''
              110  COMPARE_OP               in
              112  POP_JUMP_IF_TRUE    118  'to 118'
              114  LOAD_ASSERT              AssertionError
              116  RAISE_VARARGS_1       1  ''
            118_0  COME_FROM           112  '112'

Parse error at or near `BEGIN_FINALLY' instruction at offset 36

    def test_windows_raises_if_not_allowed--- This code section failed: ---

 L.1462         0  LOAD_GLOBAL              StreamSet
                2  LOAD_FAST                'stream1'
                4  BUILD_LIST_1          1 
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'streams'

 L.1463        10  LOAD_FAST                'streams'
               12  LOAD_METHOD              windows
               14  LOAD_CONST               8
               16  LOAD_CONST               22
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          

 L.1465        22  LOAD_GLOBAL              pytest
               24  LOAD_METHOD              raises
               26  LOAD_GLOBAL              Exception
               28  CALL_METHOD_1         1  ''
               30  SETUP_WITH           50  'to 50'
               32  STORE_FAST               'exc'

 L.1466        34  LOAD_FAST                'streams'
               36  LOAD_METHOD              windows
               38  LOAD_CONST               10
               40  LOAD_CONST               20
               42  CALL_METHOD_2         2  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  BEGIN_FINALLY    
             50_0  COME_FROM_WITH       30  '30'
               50  WITH_CLEANUP_START
               52  WITH_CLEANUP_FINISH
               54  END_FINALLY      

 L.1467        56  LOAD_STR                 'window operation is already requested'
               58  LOAD_GLOBAL              str
               60  LOAD_FAST                'exc'
               62  CALL_FUNCTION_1       1  ''
               64  LOAD_METHOD              lower
               66  CALL_METHOD_0         0  ''
               68  COMPARE_OP               in
               70  POP_JUMP_IF_TRUE     76  'to 76'
               72  LOAD_ASSERT              AssertionError
               74  RAISE_VARARGS_1       1  ''
             76_0  COME_FROM            70  '70'

Parse error at or near `BEGIN_FINALLY' instruction at offset 48

    def test_windows_returns_self(self, stream1):
        """
        Assert windows returns self
        """
        streams = StreamSet([stream1])
        result = streams.windows(10, 20)
        assert result is streams

    def test_windows_stores_values(self, stream1):
        """
        Assert windows stores values
        """
        streams = StreamSet([stream1])
        result = streams.windows(10, 20)
        assert streams.width == 10
        assert streams.depth == 20

    def test_windows_values_and_calls_to_endpoint(self):
        """
        assert windows result and endpoint calls are correct
        """
        endpoint = Mock(Endpoint)
        window1 = [[(StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6),), 11]]
        window2 = [[(StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7),), 12]]
        endpoint.windows = Mock(side_effect=[window1, window2])
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        uu2 = uuid.UUID('5d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        s1 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu1)
        s2 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu2)
        versions = {uu1: 11, uu2: 12}
        start, end, width, depth = (1, 100, 1000, 25)
        streams = StreamSet([s1, s2])
        streams.pin_versions(versions)
        values = streams.filter(start=start, end=end).windows(width=width, depth=depth).values()
        expected = [
         call(uu1, start, end, width, depth, versions[uu1]),
         call(uu2, start, end, width, depth, versions[uu2])]
        assert endpoint.windows.call_args_list == expected
        expected = [
         [
          StatPoint(1, 2.0, 3.0, 4.0, 5, 6.0)],
         [
          StatPoint(2, 3.0, 4.0, 5.0, 6, 7.0)]]
        assert values == expected

    def test_windows_rows_and_calls_to_endpoint(self):
        """
        assert windows rows result and endpoint calls are correct
        """
        endpoint = Mock(Endpoint)
        window1 = [[(StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6),), 11]]
        window2 = [[(StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7),), 12]]
        endpoint.windows = Mock(side_effect=[window1, window2])
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        uu2 = uuid.UUID('5d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        s1 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu1)
        s2 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu2)
        versions = {uu1: 11, uu2: 12}
        start, end, width, depth = (1, 100, 1000, 25)
        streams = StreamSet([s1, s2])
        streams.pin_versions(versions)
        rows = streams.filter(start=start, end=end).windows(width=width, depth=depth).rows()
        expected = [
         call(uu1, start, end, width, depth, versions[uu1]),
         call(uu2, start, end, width, depth, versions[uu2])]
        assert endpoint.windows.call_args_list == expected
        expected = [
         (
          StatPoint(1, 2.0, 3.0, 4.0, 5, 6.0), None),
         (
          None, StatPoint(2, 3.0, 4.0, 5.0, 6, 7.0))]
        assert rows == expected

    def test_aligned_windows_raises_valueerror--- This code section failed: ---

 L.1569         0  LOAD_GLOBAL              StreamSet
                2  LOAD_FAST                'stream1'
                4  BUILD_LIST_1          1 
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'streams'

 L.1570        10  LOAD_GLOBAL              pytest
               12  LOAD_METHOD              raises
               14  LOAD_GLOBAL              ValueError
               16  CALL_METHOD_1         1  ''
               18  SETUP_WITH           36  'to 36'
               20  STORE_FAST               'exc'

 L.1571        22  LOAD_FAST                'streams'
               24  LOAD_METHOD              aligned_windows
               26  LOAD_STR                 'invalid'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          
               32  POP_BLOCK        
               34  BEGIN_FINALLY    
             36_0  COME_FROM_WITH       18  '18'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

 L.1572        42  LOAD_STR                 'literal'
               44  LOAD_GLOBAL              str
               46  LOAD_FAST                'exc'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_METHOD              lower
               52  CALL_METHOD_0         0  ''
               54  COMPARE_OP               in
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  LOAD_ASSERT              AssertionError
               60  RAISE_VARARGS_1       1  ''
             62_0  COME_FROM            56  '56'

Parse error at or near `BEGIN_FINALLY' instruction at offset 34

    def test_aligned_windows_raises_if_not_allowed--- This code section failed: ---

 L.1579         0  LOAD_GLOBAL              StreamSet
                2  LOAD_FAST                'stream1'
                4  BUILD_LIST_1          1 
                6  CALL_FUNCTION_1       1  ''
                8  STORE_FAST               'streams'

 L.1580        10  LOAD_FAST                'streams'
               12  LOAD_METHOD              windows
               14  LOAD_CONST               8
               16  LOAD_CONST               22
               18  CALL_METHOD_2         2  ''
               20  POP_TOP          

 L.1582        22  LOAD_GLOBAL              pytest
               24  LOAD_METHOD              raises
               26  LOAD_GLOBAL              Exception
               28  CALL_METHOD_1         1  ''
               30  SETUP_WITH           48  'to 48'
               32  STORE_FAST               'exc'

 L.1583        34  LOAD_FAST                'streams'
               36  LOAD_METHOD              aligned_windows
               38  LOAD_CONST               20
               40  CALL_METHOD_1         1  ''
               42  POP_TOP          
               44  POP_BLOCK        
               46  BEGIN_FINALLY    
             48_0  COME_FROM_WITH       30  '30'
               48  WITH_CLEANUP_START
               50  WITH_CLEANUP_FINISH
               52  END_FINALLY      

 L.1584        54  LOAD_STR                 'window operation is already requested'
               56  LOAD_GLOBAL              str
               58  LOAD_FAST                'exc'
               60  CALL_FUNCTION_1       1  ''
               62  LOAD_METHOD              lower
               64  CALL_METHOD_0         0  ''
               66  COMPARE_OP               in
               68  POP_JUMP_IF_TRUE     74  'to 74'
               70  LOAD_ASSERT              AssertionError
               72  RAISE_VARARGS_1       1  ''
             74_0  COME_FROM            68  '68'

Parse error at or near `BEGIN_FINALLY' instruction at offset 46

    def test_aligned_windows(self, stream1):
        """
        Assert aligned_windows stores objects
        """
        streams = StreamSet([stream1])
        result = streams.aligned_windows(20)
        assert streams.pointwidth == 20

    def test_aligned_windows_returns_self(self, stream1):
        """
        Assert aligned_windows returns self
        """
        streams = StreamSet([stream1])
        result = streams.aligned_windows(20)
        assert result is streams

    def test_aligned_windows_values_and_calls_to_endpoint(self):
        """
        assert aligned_windows result and endpoint calls are correct
        """
        endpoint = Mock(Endpoint)
        window1 = [[(StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6),), 11]]
        window2 = [[(StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7),), 12]]
        endpoint.alignedWindows = Mock(side_effect=[window1, window2])
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        uu2 = uuid.UUID('5d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        s1 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu1)
        s2 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu2)
        versions = {uu1: 11, uu2: 12}
        start, end, pointwidth = (1, 100, 25)
        streams = StreamSet([s1, s2])
        streams.pin_versions(versions)
        values = streams.filter(start=start, end=end).aligned_windows(pointwidth=pointwidth).values()
        expected = [
         call(uu1, start, end, pointwidth, versions[uu1]),
         call(uu2, start, end, pointwidth, versions[uu2])]
        assert endpoint.alignedWindows.call_args_list == expected
        expected = [
         [
          StatPoint(1, 2.0, 3.0, 4.0, 5, 6.0)],
         [
          StatPoint(2, 3.0, 4.0, 5.0, 6, 7.0)]]
        assert values == expected

    def test_aligned_windows_rows_and_calls_to_endpoint(self):
        """
        assert aligned_windows rows result and endpoint calls are correct
        """
        endpoint = Mock(Endpoint)
        window1 = [[(StatPointProto(time=1, min=2, mean=3, max=4, count=5, stddev=6),), 11]]
        window2 = [[(StatPointProto(time=2, min=3, mean=4, max=5, count=6, stddev=7),), 12]]
        endpoint.alignedWindows = Mock(side_effect=[window1, window2])
        uu1 = uuid.UUID('0d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        uu2 = uuid.UUID('5d22a53b-e2ef-4e0a-ab89-b2d48fb2592a')
        s1 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu1)
        s2 = Stream(btrdb=(BTrDB(endpoint)), uuid=uu2)
        versions = {uu1: 11, uu2: 12}
        start, end, pointwidth = (1, 100, 25)
        streams = StreamSet([s1, s2])
        streams.pin_versions(versions)
        rows = streams.filter(start=start, end=end).aligned_windows(pointwidth=pointwidth).rows()
        expected = [
         call(uu1, start, end, pointwidth, versions[uu1]),
         call(uu2, start, end, pointwidth, versions[uu2])]
        assert endpoint.alignedWindows.call_args_list == expected
        expected = [
         (
          StatPoint(1, 2.0, 3.0, 4.0, 5, 6.0), None),
         (
          None, StatPoint(2, 3.0, 4.0, 5.0, 6, 7.0))]
        assert rows == expected

    def test_rows(self, stream1, stream2):
        """
        Assert rows returns correct values
        """
        stream1.values = Mock(return_value=(iter([
         (
          RawPoint(time=1, value=1), 1), (RawPoint(time=2, value=2), 1),
         (
          RawPoint(time=3, value=3), 1), (RawPoint(time=4, value=4), 1)])))
        stream2.values = Mock(return_value=(iter([
         (
          RawPoint(time=1, value=1), 2), (RawPoint(time=3, value=3), 2)])))
        streams = StreamSet([stream1, stream2])
        rows = iter(streams.rows())
        assert next(rows) == (RawPoint(time=1, value=1), RawPoint(time=1, value=1))
        assert next(rows) == (RawPoint(time=2, value=2), None)
        assert next(rows) == (RawPoint(time=3, value=3), RawPoint(time=3, value=3))
        assert next(rows) == (RawPoint(time=4, value=4), None)

    def test_params_from_filters_latest_value_wins(self, stream1):
        """
        Assert _params_from_filters returns latest setting
        """
        streams = StreamSet([stream1])
        assert streams.filters == []
        streams = streams.filter(start=1)
        assert streams._params_from_filters() == {'start': 1}
        streams = streams.filter(start=2)
        assert streams._params_from_filters() == {'start': 2}

    def test_params_from_filters_works(self, stream1):
        """
        Assert _params_from_filters returns correct values
        """
        streams = StreamSet([stream1])
        assert streams.filters == []
        streams = streams.filter(start=1, end=2)
        assert streams._params_from_filters() == {'start':1,  'end':2}
        streams = streams.filter(start=9, end=10)
        assert streams._params_from_filters() == {'start':9,  'end':10}

    def test_values(self, stream1, stream2):
        """
        Assert values returns correct data
        """
        stream1_values = [
         (
          RawPoint(time=1, value=1), 1), (RawPoint(time=2, value=2), 1),
         (
          RawPoint(time=3, value=3), 1), (RawPoint(time=4, value=4), 1)]
        stream1.values = Mock(return_value=(iter(stream1_values)))
        stream2_values = [
         (
          RawPoint(time=1, value=1), 2), (RawPoint(time=3, value=3), 2)]
        stream2.values = Mock(return_value=(iter(stream2_values)))
        streams = StreamSet([stream1, stream2])
        assert streams.values() == [
         [t[0] for t in stream1_values],
         [t[0] for t in stream2_values]]


class TestStreamFilter(object):

    def test_create(self):
        """
        Assert we can create the object
        """
        StreamFilter(0, 1)

    def test_start_larger_or_equal(self):
        """
        Assert we raise ValueError if start is greater than/equal to end
        """
        with pytest.raises(ValueError):
            StreamFilter(1, 1)

    def test_start_valid(self):
        """
        Assert we can use any value castable to an int for start argument
        """
        sf = StreamFilter(start='100')
        assert sf.start == 100
        sf = StreamFilter(start=100.0)
        assert sf.start == 100
        sf = StreamFilter(start=100)
        assert sf.start == 100

    def test_start_invalid(self):
        """
        Assert we raise ValueError if start is greater than/equal to end
        """
        with pytest.raises(ValueError):
            StreamFilter(start='foo')