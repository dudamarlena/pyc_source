# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seeta_dataset/writeonly_dataset.py
# Compiled at: 2019-10-24 15:15:30
# Size of source mod 2**32: 4658 bytes
import json, struct, os
from seeta_dataset import base

class WriteOnlyDataset:
    __doc__ = 'Create a new seeta dataset for writing seeta records\n    Args:\n        base_path: ...\n        dataset_id: ...\n        record_type: ...\n    Examples:\n    ```python\n    >>> import seeta_dataset as sd\n    >>> rt = sd.record_type.new_record_type({\n    >>>        "s": BasicType.String,\n    >>>        "i": BasicType.Int,\n    >>>        "f": BasicType.Float,\n    >>>        "l_s": [BasicType.String],\n    >>>        "l_i": [BasicType.Int],\n    >>>        "m": {\n    >>>            "x": BasicType.Int,\n    >>>            "y": BasicType.Float,\n    >>>            "s": BasicType.String,\n    >>>        },\n    >>>        "l_m": [{\n    >>>            "x": BasicType.Int,\n    >>>            "y": BasicType.Float,\n    >>>        }]\n    >>>    })\n    >>> with WriteOnlyDataset("./", "test", rt) as dataset:\n    >>>     dataset.write({\n    >>>         "s": "ssssss",\n    >>>         "i": 1,\n    >>>         "f": 1.1,\n    >>>         "l_s": ["l_s_1", "l_s_2"],\n    >>>         "l_i": [1, 2, 3],\n    >>>         "m": {\n    >>>             "x": 1,\n    >>>             "y": 1.1,\n    >>>             "s": "m.s",\n    >>>         },\n    >>>         "l_m": [{\n    >>>             "x": 1,\n    >>>             "y": 1.1,\n    >>>             "s": "m.s",\n    >>>         }, {\n    >>>             "x": 1,\n    >>>             "y": 1.1,\n    >>>             "s": "m.s",\n    >>>         }]\n    >>>     })\n    >>>\n    ```\n    '

    def __init__(self, base_path, dataset_id=None, record_type=None):
        self._base_path = base_path
        self._dataset_id = dataset_id or base.DEFAULT_DATA_NAME
        self._record_type = record_type
        self._version = 0
        meta_file_path = os.path.join(self._base_path, '{}.meta'.format(self._dataset_id))
        if os.path.exists(meta_file_path):
            raise base.FileExistError(meta_file_path)
        self._meta_file = open(meta_file_path, 'w')
        index_file_path = os.path.join(self._base_path, '{}.index'.format(self._dataset_id))
        if os.path.exists(index_file_path):
            raise base.FileExistError(index_file_path)
        self._index_file = open(index_file_path, 'wb')
        data_file_path = os.path.join(self._base_path, '{}.data'.format(self._dataset_id))
        if os.path.exists(data_file_path):
            raise base.FileExistError(data_file_path)
        self._data_file = open(data_file_path, 'wb')
        self._indexes = []
        self._current = 0

    def get_id(self):
        return self._dataset_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return
        else:
            self.close()
            return True

    def close(self):
        self._meta_file.write(json.dumps(self.dump()))
        self._meta_file.close()
        self._indexes.append(self._current)
        index_data = (struct.pack)('<{}Q'.format(len(self._indexes)), *self._indexes)
        self._index_file.write(index_data)
        self._index_file.close()
        self._data_file.close()

    def dump(self):
        return {'Version':self._version, 
         'ID':self._dataset_id, 
         'RecordType':self._record_type.dump()}

    def write(self, record):
        buffer = bytearray()
        length = self._record_type.encode(record, buffer)
        self._data_file.write(buffer)
        self._indexes.append(self._current)
        self._current += length


if __name__ == '__main__':
    from seeta_dataset.record_type import new_record_type, BasicType
    rt = new_record_type({'s':BasicType.String, 
     'i':BasicType.Int, 
     'f':BasicType.Float, 
     'l_s':[
      BasicType.String], 
     'l_i':[
      BasicType.Int], 
     'm':{'x':BasicType.Int, 
      'y':BasicType.Float, 
      's':BasicType.String}, 
     'l_m':[
      {'x':BasicType.Int, 
       'y':BasicType.Float}], 
     'b':BasicType.ByteArray})
    with WriteOnlyDataset('.', 'test', rt) as (dataset):
        dataset.write({'s':'ssssss', 
         'i':1, 
         'f':1.1, 
         'l_s':[
          'l_s_1', 'l_s_2'], 
         'l_i':[
          1, 2, 3], 
         'm':{'x':1, 
          'y':1.1, 
          's':'m.s'}, 
         'l_m':[
          {'x':1, 
           'y':1.1, 
           's':'m.s'},
          {'x':1, 
           'y':1.1, 
           's':'m.s'}], 
         'b':bytes(b'abcdefg')})
    print('done')