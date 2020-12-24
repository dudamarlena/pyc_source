# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/btrdb/utils/test_conversions.py
# Compiled at: 2019-08-01 15:53:35
# Size of source mod 2**32: 3767 bytes
__doc__ = '\nTesting for btrdb convertion utilities\n'
import uuid, json, pytest, numpy as np
from datetime import datetime
from btrdb.utils.conversion import to_uuid
from btrdb.utils.conversion import AnnotationDecoder, AnnotationEncoder
EXAMPLE_UUID_STR = '07d28a44-4991-492d-b9c5-2d8cec5aa6d4'
EXAMPLE_UUID_BYTES = EXAMPLE_UUID_STR.encode('ASCII')
EXAMPLE_UUID = uuid.UUID(EXAMPLE_UUID_STR)

class TestAnnotationJSON(object):

    @pytest.mark.parametrize('obj, expected', [
     (True, 'true'),
     (False, 'false'),
     (None, 'null'),
     (3.14, '3.14'),
     (42, '42'),
     ('foo', 'foo'),
     ('a long walk on the beach', 'a long walk on the beach'),
     (
      [
       'a', 'b', 'c'], '["a", "b", "c"]'),
     (
      {'color':'red', 
       'foo':24}, '{"color": "red", "foo": 24}'),
     (
      datetime(2018, 9, 10, 16, 30), '2018-09-10 16:30:00.000000'),
     (
      np.datetime64(datetime(2018, 9, 10, 16, 30)), '2018-09-10 16:30:00.000000+0000'),
     (
      EXAMPLE_UUID, EXAMPLE_UUID_STR)])
    def test_annotations_encoder(self, obj, expected):
        msg = f"did not correctly encode type {type(obj)}"
        assert json.dumps(obj, cls=AnnotationEncoder, indent=None) == expected, msg

    @pytest.mark.parametrize('obj, s', [
     (True, 'true'),
     (False, 'false'),
     (None, 'null'),
     (3.14, '3.14'),
     (42, '42'),
     ('foo', 'foo'),
     ('foo', '"foo"'),
     ('a long walk on the beach', 'a long walk on the beach'),
     ('a long walk on the beach', '"a long walk on the beach"'),
     (
      [
       'a', 'b', 'c'], '["a", "b", "c"]'),
     (
      {'color':'red', 
       'foo':24}, '{"color": "red", "foo": 24}'),
     ('2018-09-10 16:30:00.000000', '2018-09-10 16:30:00.000000'),
     (
      {'uuid': EXAMPLE_UUID_STR}, f'{{"uuid": "{EXAMPLE_UUID_STR}"}}')])
    def test_annotations_decoder(self, obj, s):
        msg = f"did not correctly decode type {type(obj)}"
        assert json.loads(s, cls=AnnotationDecoder) == obj, msg


class TestToUUID(object):

    def test_from_bytes(self):
        """
        Assert that `to_uuid` converts from bytes
        """
        assert to_uuid(EXAMPLE_UUID_BYTES) == EXAMPLE_UUID

    def test_from_str(self):
        """
        Assert that `to_uuid` converts from str
        """
        assert to_uuid(EXAMPLE_UUID_STR) == EXAMPLE_UUID

    def test_from_uuid(self):
        """
        Assert that `to_uuid` returns passed UUID
        """
        assert to_uuid(EXAMPLE_UUID) == EXAMPLE_UUID

    def test_raises_on_bad_data(self):
        """
        Assert that `to_uuid` raises error with bad UUID string
        """
        with pytest.raises(ValueError):
            to_uuid('bad data!!!')

    def test_raises_on_incorrect_input_type--- This code section failed: ---

 L. 112         0  LOAD_GLOBAL              pytest
                2  LOAD_METHOD              raises
                4  LOAD_GLOBAL              TypeError
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           24  'to 24'
               10  STORE_FAST               'exc'

 L. 113        12  LOAD_GLOBAL              to_uuid
               14  LOAD_CONST               3.0
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          
               20  POP_BLOCK        
               22  BEGIN_FINALLY    
             24_0  COME_FROM_WITH        8  '8'
               24  WITH_CLEANUP_START
               26  WITH_CLEANUP_FINISH
               28  END_FINALLY      

 L. 115        30  LOAD_STR                 'Cannot convert object to UUID'
               32  LOAD_GLOBAL              str
               34  LOAD_FAST                'exc'
               36  CALL_FUNCTION_1       1  ''
               38  COMPARE_OP               in
               40  POP_JUMP_IF_TRUE     46  'to 46'
               42  LOAD_ASSERT              AssertionError
               44  RAISE_VARARGS_1       1  ''
             46_0  COME_FROM            40  '40'

 L. 116        46  LOAD_STR                 'float'
               48  LOAD_GLOBAL              str
               50  LOAD_FAST                'exc'
               52  CALL_FUNCTION_1       1  ''
               54  COMPARE_OP               in
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  LOAD_ASSERT              AssertionError
               60  RAISE_VARARGS_1       1  ''
             62_0  COME_FROM            56  '56'

Parse error at or near `BEGIN_FINALLY' instruction at offset 22