# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/json_encoders/RefJSONEncoder.py
# Compiled at: 2020-05-11 02:48:33
# Size of source mod 2**32: 2388 bytes
import json
from collections import OrderedDict
from enum import Enum
from .utils import is_elemental, is_collection, is_custom_class, hashable

class RefJSONEncoder(json.JSONEncoder):

    def _count_ref(self, obj):
        if is_elemental(obj):
            return
        if is_collection(obj):
            self._count_ref_in_collection(obj)
        else:
            if is_custom_class(obj):
                if hashable(obj):
                    if obj in self.cls_ref_cnt:
                        self.cls_ref_cnt[obj] += 1
                    else:
                        self.cls_ref_cnt[obj] = 1
                    for name, value in obj.__dict__.items():
                        self._count_ref(value)

    def _count_ref_in_collection--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'obj'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L.  23        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.  24        16  LOAD_GLOBAL              isinstance
               18  LOAD_FAST                'obj'
               20  LOAD_GLOBAL              list
               22  LOAD_GLOBAL              tuple
               24  LOAD_GLOBAL              set
               26  BUILD_TUPLE_3         3 
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  POP_JUMP_IF_FALSE    58  'to 58'

 L.  25        32  SETUP_LOOP          100  'to 100'
               34  LOAD_FAST                'obj'
               36  GET_ITER         
               38  FOR_ITER             54  'to 54'
               40  STORE_FAST               'item'

 L.  26        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _count_ref
               46  LOAD_FAST                'item'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  POP_TOP          
               52  JUMP_BACK            38  'to 38'
               54  POP_BLOCK        
               56  JUMP_FORWARD        100  'to 100'
             58_0  COME_FROM            30  '30'

 L.  27        58  LOAD_GLOBAL              isinstance
               60  LOAD_FAST                'obj'
               62  LOAD_GLOBAL              dict
               64  CALL_FUNCTION_2       2  '2 positional arguments'
               66  POP_JUMP_IF_FALSE   100  'to 100'

 L.  28        68  SETUP_LOOP          100  'to 100'
               70  LOAD_FAST                'obj'
               72  LOAD_METHOD              items
               74  CALL_METHOD_0         0  '0 positional arguments'
               76  GET_ITER         
               78  FOR_ITER             98  'to 98'
               80  UNPACK_SEQUENCE_2     2 
               82  STORE_FAST               'k'
               84  STORE_FAST               'v'

 L.  29        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _count_ref
               90  LOAD_FAST                'v'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_TOP          
               96  JUMP_BACK            78  'to 78'
               98  POP_BLOCK        
            100_0  COME_FROM_LOOP       68  '68'
            100_1  COME_FROM            66  '66'
            100_2  COME_FROM            56  '56'
            100_3  COME_FROM_LOOP       32  '32'

Parse error at or near `COME_FROM' instruction at offset 100_2

    def _prepare(self, o):
        self.cls_ref_cnt = {}
        self.cls_ref_serialized = {}
        self.ref_id = 0

    def encode(self, o):
        return super().encode(o)

    def iterencode(self, o, _one_shot=False):
        self._prepare(o)
        self._count_ref(o)
        return super().iterencode(o, _one_shot)

    def default(self, obj):
        if isinstanceobjset:
            return list(obj)
        if isinstanceobjEnum:
            return obj.value
        if is_custom_class(obj):
            return self._process_custom_cls(obj)
        return obj

    def _process_custom_cls(self, obj):
        if not hashable(obj) or obj not in self.cls_ref_cnt or self.cls_ref_cnt[obj] <= 1:
            return {k:v for k, v in obj.__dict__.items() if v is not None if v is not None}
            if obj in self.cls_ref_serialized:
                return {'$ref': str(self.cls_ref_serialized[obj])}
            if self.cls_ref_cnt[obj] > 1:
                self.ref_id += 1
                self.cls_ref_serialized[obj] = self.ref_id
                out = OrderedDict()
                out['$id'] = str(self.ref_id)
                for k, v in obj.__dict__.items():
                    if v is None:
                        continue
                    out[k] = v

                return out
        raise Exception('Unhandled custom class obj in _process_custom_cls')