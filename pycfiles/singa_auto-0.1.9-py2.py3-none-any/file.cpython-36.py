# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/param_store/file.py
# Compiled at: 2020-04-15 05:36:06
# Size of source mod 2**32: 1907 bytes
import os, uuid
from .param_store import ParamStore, Params

class FileParamStore(ParamStore):
    __doc__ = '\n       Stores parameters in the local filesystem.\n    '

    def __init__(self, params_dir=None):
        self._params_dir = params_dir or os.path.join(os.environ['WORKDIR_PATH'], os.environ['PARAMS_DIR_PATH'])

    def save(self, params: Params):
        file_name = '{}.model'.format(uuid.uuid4())
        dest_file_path = os.path.join(self._params_dir, file_name)
        params_bytes = self._serialize_params(params)
        with open(dest_file_path, 'wb') as (f):
            f.write(params_bytes)
        params_id = file_name
        return params_id

    def load(self, params_id):
        file_name = params_id
        file_path = os.path.join(self._params_dir, file_name)
        with open(file_path, 'rb') as (f):
            params_bytes = f.read()
        params = self._deserialize_params(params_bytes)
        return params