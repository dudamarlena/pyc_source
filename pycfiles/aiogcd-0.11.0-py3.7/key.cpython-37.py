# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/connector/key.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 4854 bytes
"""key.py

Created on: May 19, 2017
    Author: Jeroen van der Heijden <jeroen@transceptor.technology>
"""
import base64
from .buffer import Buffer
from .buffer import BufferDecodeError
from .path import Path
from .path import path_from_decoder
from .decoder import Decoder

class Key:
    KEY_INIT_MSG = '\n        Key can be initialized by using a dictionary, for example:\n\n            Key({\n                "partitionId": {\n                    "projectId": "my-project-id"\n                },\n                "path": [{\n                  "kind": "Foo",\n                  "id": "12345678"\n                }]\n            })\n\n        Or by using a key string, for example:\n\n            Key(ks="ag9zfm15LXByb2plY3QtaWRyDAsSA0ZvbxjOwvEFDA")\n\n        Or, you can use arguments and set a project_id, for example:\n\n            Key("Foo", 12345678, ..., project_id="my-project-id")\n\n        Or you can use keyword arguments path and project_id, for example:\n\n            Key(path=Path(...), project_id="my-project-id")\n'
    _ks = None

    def __init__(self, *args, ks=None, path=None, project_id=None):
        if len(args) == 1:
            if isinstance(args[0], dict):
                if not (ks is None and path is None and project_id is None):
                    raise AssertionError(self.KEY_INIT_MSG)
                res = args[0]
                self.project_id = res['partitionId']['projectId']
                self.path = Path(pairs=(tuple(((pair['kind'], self._extract_id_or_name(pair)) for pair in res['path']))))
                return
        if ks is not None and not args:
            if not (path is None and project_id is None):
                raise AssertionError(self.KEY_INIT_MSG)
            self.project_id, self.path = self._deserialize_ks(ks)
            return
            if not (project_id is not None and (not args) ^ (path is None)):
                raise AssertionError(self.KEY_INIT_MSG)
            if not len(args) % 2 == 0:
                raise AssertionError(self.KEY_INIT_MSG)
        self.project_id = project_id
        self.path = Path(pairs=zip(*[iter(args)] * 2)) if path is None else path

    def get_path(self):
        return self.path.get_as_tuple()

    def __repr__(self):
        return self.path.__repr__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.ks == other.ks
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def encode(self):
        """Return a Buffer() object which is a byte-like object.

        For serializing the key object you can use the .ks property which uses
        this method for generating an urlsafe key string.
        """
        buffer = Buffer()
        buffer.add_var_int32(106)
        buffer.add_prefixed_string('s~{}'.format(self.project_id))
        self.path.encode(buffer)
        return buffer

    @property
    def ks(self):
        if self._ks is None:
            self._ks = base64.b64encode(self.encode()).rstrip(b'=').replace(b'+', b'-').replace(b'/', b'_').decode('utf-8')
        return self._ks

    def get_dict(self):
        d = {'partitionId': {'projectId': self.project_id}}
        d.update(self.path.get_dict())
        return d

    @property
    def kind(self):
        """Shortcut for .path[-1].kind"""
        return self.path[(-1)].kind

    @property
    def id(self):
        """Shortcut for .path[-1].id"""
        return self.path[(-1)].id

    @staticmethod
    def _extract_id_or_name(pair):
        """Used on __init__."""
        if 'id' in pair:
            return int(pair['id'])
        if 'name' in pair:
            return pair['name']

    @staticmethod
    def _deserialize_ks(ks):
        """Returns a Key() object from a key string."""
        decoder = Decoder(ks=ks)
        project_id = None
        path = None
        while decoder:
            tt = decoder.get_var_int32()
            if tt == 106:
                project_id = decoder.get_prefixed_string()[2:]
                continue
            if tt == 114:
                l = decoder.get_var_int32()
                decoder.set_end(l)
                path = path_from_decoder(decoder)
                decoder.set_end()
                continue
            if tt == 162:
                raise BufferDecodeError('namespaces are not supported')
            if tt == 0:
                raise BufferDecodeError('corrupt')

        return (
         project_id, path)

    def get_parent(self):
        parent_pairs = self.path.get_as_tuple()[:-1]
        parent_path = Path(pairs=parent_pairs)
        return Key(path=parent_path, project_id=(self.project_id))